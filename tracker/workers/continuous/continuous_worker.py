import os
import time
import random
import celery
import urllib
import ssl
import re
import gc
import pdftotext
import fastText
import celery

import tracker.celery_continuous_conf as celeryconf
import tracker.core.utils as utils
import tracker.core.scrapper as scrapper
import tracker.core.extractor as extractor
# from tracker.celery import app
from tracker.mail import mail_sbb

# Hack to load only necessary modules (pb with ml model)
# TODO: Replace raw path with os.environ ($APP_DIR)
# TODO: Look at __init__.py to load it more properly
print('FILE continuous == {}'.format(__file__))
if '.egg' in __file__ and  'workers/continuous' in os.getcwd():
    import tracker.ml_toolbox as mltx
    su_model = mltx.SU_Model('trained_800_wiki2.bin').su_model
    already_visited = list()
    already_seen_content = list()

app = celery.Celery(__name__) # TODO : Change to sth like 'permanent listener'
app.config_from_object(celeryconf)

def make_predictions(content, min_acc=0.75):
    global su_model
    #print('su_model : {}'.format(su_model))
    #gc.collect()
    print('content : {} [...]'.format(content[:1000]))
    preds = su_model.predict(content, 2)
    print('predictions = {}'.format(preds))
    #print('predictions = {} (acc = {})'.format(preds[0][0], preds[1][0]))
    if '__label__1' in preds[0][0] and preds[1][0] > min_acc:
        prediction = '__label__1'
        print('[FastText] Predicted {} with {} confidence.'.format(prediction, preds[1][0]))
        return True
    else:
        prediction = '__label__2'
        print('[FastText] Predicted {} with {} confidence.'.format(prediction, preds[1][0]))
        return False

def is_sbb_content(url, language='ENGLISH', min_acc=0.8):
    if ('@' or ':') in url:
        return False
    global su_model
    global already_visited
    global already_seen_content

    print('ENTER CHECK SBB : {}'.format(url))
    #global su_model
    req = urllib.request.Request(
            url,
            data=None,
            headers=utils.rh()
    )
    # Faking SSL certificate to avoid unauthorized requests
    gcontext = ssl._create_unverified_context()
    try:
        response = urllib.request.urlopen(req, context=gcontext)
    except Exception as e:
        print('-- [ERROR FETCHING URL {}] --\nReason:{}\n'.format(url, e))
        return False

    if response.geturl() != url:
        print('//////////// {} has been redirected to : {} //////////'.format(response.geturl(), url))
        url = response.geturl()
        if url in already_visited:
            return False
        already_visited.append(url)

    filename = url.rpartition('/')[2]

    # get header charset
    info = response.info()
    cs = info.get_content_type()

    if extractor.is_valid_file(filename) or 'pdf' in cs:
        #print('URL = {} (detected pdf)'.format(url))
        cleaned_content = extractor.clean_pdf_content(pdftotext.PDF(response))
        #print('cleaned content url {} = {}'.format(url, cleaned_content[:50]))
        if cleaned_content is None or cleaned_content in already_seen_content:
            #print('Content {} is None !!!!!!!!!'.format(url))
            return False
        already_seen_content.append(cleaned_content)
        # if not extractor.is_language(cleaned_content, 'ENGLISH'):
        #     print('Language is NOT ENGLISH !! (Content = {}...)'.format(cleaned_content[:100]))
        #     return False
        return make_predictions(cleaned_content, min_acc=min_acc)

    else:
        print('URL = {} (detected NON pdf)'.format(url))
        cleaned_content = extractor.get_essential_content(response.read(), 10)

        if cleaned_content is None or cleaned_content in already_seen_content:
            #print('Content {} is None !!!!!!!!!'.format(url))
            return False
        already_seen_content.append(cleaned_content)
        #content = extractor.extract_text_from_html(response.read())
        #cleaned_content = extractor.clean_content(content)
        #print('Content to analyse = {}'.format(cleaned_content[:100]))
        # if not extractor.is_language(cleaned_content, 'ENGLISH'):
        #     print('Language is NOT ENGLISH (non pdf) !! (Content = {}...)'.format(cleaned_content[:100]))
        #     return False
        return make_predictions(cleaned_content, min_acc=min_acc)

    return False

def select_only_sbb_links(status):
    print('\n-------------------------------———\n')
    i = 0
    excluded_links = list()
    for link in status['all_links_pos'].copy():
        if is_sbb_content(link) is False:
            excluded_links.append(link)
            status['all_links_pos'].remove(link)#(index)
    for link in status['all_links_neg'].copy():
        if is_sbb_content(link) is False:
            excluded_links.append(link)
            status['all_links_neg'].remove(link)
    for link in status['nearest_link_pos'].copy():
        if is_sbb_content(link) is False:
            excluded_links.append(link)
            status['nearest_link_pos'].remove(link)
    for link in status['nearest_link_neg'].copy():
        if is_sbb_content(link) is False:
            excluded_links.append(link)
            status['nearest_link_neg'].remove(link)
    print('Excluded links are :\n')
    for _ in excluded_links:
        print(_)
    print('\n-------------------------------———\n')
    return status

def get_full_links(status, base_url):
    keys = ['nearest_link_pos', 'nearest_link_neg', 'all_links_pos', 'all_links_neg']
    for _ in keys:
        if status[_] != []:
            idx = 0
            for x in status[_]:
                if x.startswith(base_url) is False:
                    if x.startswith('http') is False:
                        status[_][idx] = base_url + x
                    else:
                        status[_][idx] = x
                idx += 1
    #print('RETURNED ALL LINKS POS = {} (len = {})'.format(status['all_links_pos'], len(status['all_links_pos'])))
    return status 

@app.task(bind=True, ignore_result=False, soft_time_limit=120)
def check_diff_delayed(self, links, base_path, diff_path, url):
    """ Try to download website parts that have changed """
    # VAL = [['/en/investors/stock-and-shareholder-corner/buyback-programs', ['DAILY DETAILS FOR THE PERIOD']]]
    #random.shuffle(links)
    print('/FILE FROM\\ == {}'.format(__file__))
    total = len(links)
    i = 0
    # print('LINKS ------> {}'.format(links))
    # print('base_path ------> {}'.format(base_path))
    # print('diff_path ------> {}'.format(diff_path))
    # print('url ------> {}'.format(url))
    for link in links:
        keywords = link[1]
        link = link[0]
        status = {
            'url': url + utils.find_internal_link(link),
            'div': url.split('//')[-1].split('/')[0],
            'diff_neg': list(),
            'diff_pos': list(),
            'nearest_link_pos': list(),
            'nearest_link_neg': list(),
            'all_links_pos': None,
            'all_links_neg': None,
            'diff_nb': 0
        }
        i += 1
        #time.sleep(random.randint(0, 10))
        base_dir_path = os.path.join(base_path, utils.find_internal_link(link).rpartition('/')[0][1:])
        filename = link.rpartition('/')[2]
        base_dir_path_file = os.path.join(base_dir_path, filename)

        # check whether adding 'unknown' is right ...
        if os.path.isdir(base_dir_path_file) and os.path.isfile(base_dir_path_file + 'unknown___'):
            base_dir_path_file = base_dir_path_file + 'unknown___'

        # getting local and remote content
        print('\n-> Fetching local content from : {}'.format(base_dir_path_file))
        print('-> Fetching remote content from : {}'.format(status['url']))
        local_content = scrapper.get_local_content(base_dir_path_file, 'rb')
        remote_content = scrapper.get_url_content(status['url'], header=utils.rh())

        if local_content is None or remote_content is None:
            print('Problem fetching local content or remote content.')
        else:
            status = extractor.get_text_diff(local_content, remote_content, status)
            # if a list of keywords is provided, only get diff that matches keywords
            if keywords != []:
                status = extractor.keyword_match(keywords, status, remote_content, url)
                print('******* len status all linsk pos 1: {}'.format(len(status['all_links_pos'])))
                status = get_full_links(status, url)
            #print('******* len status all linsk pos 2: {}'.format(len(status['all_links_pos'])))
            status = select_only_sbb_links(status)

            # taking off doublons in diff pos and diff neg
            status['diff_pos'] = [x.strip() for x in status['diff_pos'].copy()]
            status['diff_neg'] = [x.strip() for x in status['diff_neg'].copy()]
            status['diff_pos'] = list(set(status['diff_pos'].copy()))
            status['diff_neg'] = list(set(status['diff_neg'].copy()))

            #print('******* len status all linsk pos 3: {}'.format(len(status['all_links_pos'])))
            self.update_state(state='PROGRESS', meta={'current': i, 'total': total, 'status': status})
            #time.sleep(3)
            
            print('\n\n ({}) DIFF POS:\n{}'.format(url, status['diff_pos']))
            print('\n\n ({}) DIFF NEG :\n{}'.format(url, status['diff_neg']))
            #exit(0)
            if len(status['diff_pos']) > 0 or len(status['diff_neg']) > 0:
                print('***** Content is different *****')
                status['diff_nb'] += 1
            else:
                print('***** Content is SIMILAR *****')

    return {'current': 100, 'total': 100, 'status': status, 'result': status['diff_nb']}


@app.task(bind=True)
def send_mails(self, task_results):
    print('ALL TASKS EXECUTED !!! ;) END END END END . RET = {}\n-----> Checking diff for email now .....'\
        .format(task_results))
    task_results = [r['status'] for r in task_results.copy() if r['status']['diff_neg'] != []\
                     or r['status']['diff_pos'] != []]
    # if task_results == []:
    #   print('No email to be sent because no diff found.')
    # else:
    mail_sbb(task_results, "simon.sicard@gmail.com")

@app.task(bind=True)
def sum_up_finish(self, add):
    #print('ARGS SENT ==> {}'.format([[k[0], k[1], k[2], k[3]] for k in add]))
    return celery.chord((check_diff_delayed.s(k[0], k[1], k[2], k[3]) for k in add), send_mails.s())()


