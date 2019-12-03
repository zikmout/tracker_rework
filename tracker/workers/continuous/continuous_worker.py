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
import json

from celery.exceptions import SoftTimeLimitExceeded
import math
from tornado import httpclient
import tracker.celery_continuous_conf as celeryconf
import tracker.core.utils as utils
import tracker.core.scrapper as scrapper
import tracker.core.extractor as extractor
# from tracker.core.rproject import RProject
# from tracker.celery import app
from tracker.mail import simple_mail_sbb, designed_mail_sbb, generic_mail_template
# from tracker.models import Project, User
from celery import Celery, group, states
from celery.backends.redis import RedisBackend

already_visited = list()
already_seen_content = list()

def patch_celery():
    """Patch redis backend."""
    def _unpack_chord_result(
        self, tup, decode,
        EXCEPTION_STATES=states.EXCEPTION_STATES,
        PROPAGATE_STATES=states.PROPAGATE_STATES,
    ):
        _, tid, state, retval = decode(tup)

        if state in EXCEPTION_STATES:
            retval = self.exception_to_python(retval)
        if state in PROPAGATE_STATES:
            # retval is an Exception
            return '{}: {}'.format(retval.__class__.__name__, str(retval))

        return retval

    celery.backends.redis.RedisBackend._unpack_chord_result = _unpack_chord_result

    return celery

app = patch_celery().Celery(__name__) # TODO : Change to sth like 'permanent listener'
app.config_from_object(celeryconf)



def make_request_for_updating_content(user_email, project_name, urls):
    # Making synchronous HTTP Request (because workers are aynchronous already)
    post_data = { 'user_email': user_email, 'project_name': project_name, 'urls': urls }
    body = json.dumps(post_data)

    http_client = httpclient.HTTPClient()
    try:
        response = http_client.fetch('http://localhost:5567/api/v1/update-content', method='POST', body=body)
        #print('RESPONSE => {}'.format(response.body))
        http_client.close()
        return response.body
    # except httpclient.HTTPError as e:
    #     print('HTTPError -> {}'.format(e))
    #     http_client.close()
    #     return json.dumps({ 'error': '{}'.format(e)})
    except Exception as e:
        print('Error -> {}'.format(e))
        http_client.close()
        return json.dumps({ 'error': '{}'.format(e)})
    

def make_request_for_predictions(content, min_acc=0.75):
    # Making synchronous HTTP Request (because workers are aynchronous already)
    post_data = { 'content': content, 'min_acc': min_acc }
    body = urllib.parse.urlencode(post_data)

    http_client = httpclient.HTTPClient()
    try:
        response = http_client.fetch('http://localhost:5567/api/v1/predict/is_sbb', method='POST', body=body)
        #print('RESPONSE => {}'.format(response.body))
        http_client.close()
        return response.body
    except httpclient.HTTPError as e:
        print('HTTPError -> {}'.format(e))
        http_client.close()
    except Exception as e:
        print('Error -> {}'.format(e))
        http_client.close()
    return json.dumps({ 'error': '{}'.format(e)})

def is_sbb_content(url, language='ENGLISH', min_acc=0.8):
    # TODO: Add more characters
    if ('@' or ':') in url:
        return False

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
        #print('-- [ERROR FETCHING URL {}] --\nReason:{}\n'.format(url, e))
        return False

    if response.geturl() != url:
        print('** {} has been redirected to : {} **'.format(response.geturl(), url))
        url = response.geturl()
        if url in already_visited:
            return False
        already_visited.append(url)

    filename = url.rpartition('/')[2]

    # get header charset
    info = response.info()
    cs = info.get_content_type()

    if extractor.is_valid_file(filename) or 'pdf' in cs:
        print('URL = {} (detected pdf)'.format(url))
        extracted = pdftotext.PDF(response)
        cleaned_content = extractor.clean_pdf_content(extracted)
        #print('cleaned content url {} = {}'.format(url, cleaned_content[:50]))
        if cleaned_content is None or cleaned_content in already_seen_content:
            #print('Content {} is None !!!!!!!!!'.format(url))
            return False
        already_seen_content.append(cleaned_content)
        # if not extractor.is_language(cleaned_content, 'ENGLISH'):
        #     print('Language is NOT ENGLISH !! (Content = {}...)'.format(cleaned_content[:100]))
        #     return False
        resp = make_request_for_predictions(cleaned_content, min_acc=min_acc)
        #print('RESPONSE 1 = {}'.format(resp))
        return json.loads(resp)

    else:
        # if 'www.facebook.' or 'www.twitter.' or 'www.youtube.' in url:
        #     return False
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
        resp = make_request_for_predictions(cleaned_content, min_acc=min_acc)
        #print('RESPONSE 2 = {}'.format(resp))
        return json.loads(resp)

    return False

def select_only_sbb_links(status):
    #print('\n-------------------------------———\n')
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
    #print('Excluded links are :\n')
    #for _ in excluded_links:
    #    print(_)
    #print('\n-------------------------------———\n')
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

@app.task(bind=True)
def bad_task(self):
    print('start bad task')
    time.sleep(10)
    print('stop sleep')

@app.task(bind=True, ignore_result=False, soft_time_limit=60)#, time_limit=121)
def get_diff(self, links, base_path, diff_path, url, keywords_diff, detect_links, links_algorithm):
    """ Download website parts that have changed 
        -> diff based on keyword matching
        -> links identified with ml algorithm that detect share buy back content (pdf or raw text)
    """
    # VAL = [['/en/investors/stock-and-shareholder-corner/buyback-programs', ['DAILY DETAILS FOR THE PERIOD']]]
    # trying to hide scrapping patterns
    random.shuffle(links)
    total = len(links)
    i = 0
    # print('before task. sleeping now. self = {}'.format(self.__dict__))
    # time.sleep(random.randint(0, 10))
    # print('after task')
    # print('LINKS ------> {}'.format(links))
    # print('base_path ------> {}'.format(base_path))
    # print('diff_path ------> {}'.format(diff_path))
    # print('url ------> {}'.format(url))
    for link in links:
        keywords = link[1] if keywords_diff else []
        link = link[0]
        flink = url + utils.find_internal_link(link)
        i += 1
        status = {
            'url': flink,
            'div': url.split('//')[-1].split('/')[0],
            'diff_neg': list(),
            'diff_pos': list(),
            'nearest_link_pos': list(),
            'nearest_link_neg': list(),
            'all_links_pos': list(),
            'all_links_neg': list(),
            'diff_nb': 0,
            'errors': dict()
        }
        try:
            
            # print('[{}/{}] Link = {}'.format(i, len(links), flink))
            #time.sleep(random.randint(0, 10))
            base_dir_path = os.path.join(base_path, utils.find_internal_link(link).rpartition('/')[0][1:])
            filename = link.rpartition('/')[2]
            base_dir_path_file = os.path.join(base_dir_path, filename)

            # check whether adding 'unknown' is right ...
            if os.path.isdir(base_dir_path_file) and os.path.isfile(base_dir_path_file + 'unknown___'):
                base_dir_path_file = base_dir_path_file + 'unknown___'

            # getting local and remote content
            #print('\n-> Fetching local content from : {}'.format(base_dir_path_file))
            #print('-> Fetching remote content from : {}'.format(status['url']))
            local_content = scrapper.get_local_content(base_dir_path_file, 'rb')
            remote_content, error_remote_content = scrapper.get_url_content(status['url'], header=utils.rh())

            if local_content is None:
                print('!!!! Problem fetching local content !!!! (url:{})'.format(flink))
                # TODO: Log errors from local content here and put in status just like for remote content
                status['errors'].update({status['url']: 'Error fetching local content'})
            if remote_content is None:
                print('!!!! Problem fetching remote content. !!!! ERROR = {}'.format(error_remote_content))
                status['errors'].update(error_remote_content)
            elif local_content is not None:
                status = extractor.get_text_diff(local_content, remote_content, status,\
                    detect_links=detect_links)
                # if a list of keywords is provided, only get diff that matches keywords
                if keywords != [] and not isinstance(keywords[0], float):
                    status = extractor.keyword_match(keywords, status, remote_content, url,\
                        detect_links=detect_links)
                    #print('******* len status all linsk pos 1: {}'.format(len(status['all_links_pos'])))
                    # if detect_links:
                        
                #print('******* len status all linsk pos 2: {}'.format(len(status['all_links_pos'])))
                if detect_links:
                    status = get_full_links(status, url)
                    status = select_only_sbb_links(status)

                #print('******* len status all linsk pos 3: {}'.format(len(status['all_links_pos'])))
                self.update_state(state='PROGRESS', meta={'current': i, 'total': total, 'status': status})
                
                #print('\n\n ({}) DIFF POS:\n{}'.format(url, status['diff_pos']))
                #print('\n\n ({}) DIFF NEG :\n{}'.format(url, status['diff_neg']))
                if len(status['diff_pos']) > 0 or len(status['diff_neg']) > 0:
                    print('***** Content is DIFFERENT ({}) *****'.format(flink))
                    status['diff_nb'] += 1
                else:
                    #print('***** Content is SIMILAR *****')
                    pass
                # return {'current': 100, 'total': 100, 'status': status, 'result': status['diff_nb']}
        except Exception as e:
            # pass
            # status['diff_nb'] = 0
            print("Share buy back diff exception => {}".format(e))
            status['errors'].update({status['url'] : '{}'.format(e)})
            return {'current': 100, 'total': 100, 'status': status, 'result': status['diff_nb']}
    return {'current': 100, 'total': 100, 'status': status, 'result': status['diff_nb']}


###################################### SBB SCHEDULED ROUTINE ######################################
@app.task(bind=True)
def log_error_sbb(self, z):
    print('ERROR for share_buy_back_task = {}'.format(z))

@app.task(bind=True)
def sbb_end_routine(self, task_results, mails, user_email, project_name):#, soft_time_limit=120):
    task_results_successful = [r['status'] for r in task_results.copy() if (r['status']['diff_neg'] != []\
                     or r['status']['diff_pos'] != [])]
    errors = dict()
    for task in task_results.copy():
        if task['status']['errors'] != {}:
            errors.update(task['status']['errors'])
    # errors = [r['errors'] for r in task_results.copy()]
    print('\ntask result = {}, \n\nerrors : {}'.format(task_results_successful.copy(), errors))
    # if task_results == []:
    #   print('No email to be sent because no diff found.')
    # else:
    if mails is None:
        print('----> SBB_END_ROUTINE <---- \n(RET = {})\n-----> No mail to be send .....'\
        .format(task_results))
    else:
        print('----> SBB_END_ROUTINE <---- \n(RET = {})\n-----> Sending mail with diff template now .....'\
        .format(task_results))
        print("SBB MAILS TEMPLATE CONTENT : {}".format(mails))
        #simple_mail_sbb(task_results, "simon.sicard@gmail.com")
        generic_mail_template(task_results_successful, errors, mails, 'sbb task', len(task_results), show_links=True)
        print('- Mails successfully sent if any changed noticed -')
    print("SBB MAILS TEMPLATE CONTENT : {}".format(mails))
    
    # Updating and download content now ...
    urls = [x['url'] for x in task_results_successful]
    make_request_for_updating_content(user_email, project_name, urls)
    print('All links ({}) successfully updated ! Yeay ! :)) '.format([x['url'] for x in task_results_successful]))

@app.task(bind=True)
def share_buy_back_task(self, add, mails, user_email, project_name):
    #print('ARGS SENT ==> {}'.format([[k[0], k[1], k[2], k[3]] for k in add]))
    #.set(
                # soft_time_limit=1
            # )
    return (group(get_diff.s(k[0], k[1], k[2], k[3], k[4], k[5], k[6]) for k in add) | diff_with_keywords_end_routine.s(mails, user_email, project_name)).delay()
    # return celery.chord((get_diff.s(k[0], k[1], k[2], k[3], k[4], k[5], k[6]\
    #     ).on_error(log_error_sbb.s()) for k in add), sbb_end_routine.s(mails, user_email, project_name))()
    # return celery.chord((get_diff.s(k[0], k[1], k[2], k[3], k[4], k[5], k[6]\
        # ).set(soft_time_limit=500) for k in add), sbb_end_routine.s(mails, user_email, project_name))()

###################################################################################################



###################################### DIFF SCHEDULED ROUTINE #####################################
@app.task(bind=True)
def log_error_diff(self, z):
    print('ERROR for diff_with_keywords_task = {}'.format(z))

@app.task(bind=True)
def diff_end_routine(self, task_results, mails, user_email, project_name):#, soft_time_limit=120):
    task_results_successful = [r['status'] for r in task_results.copy() if (r['status']['diff_neg'] != []\
                     or r['status']['diff_pos'] != [])]
    errors = dict()
    for task in task_results.copy():
        if task['status']['errors'] != {}:
            errors.update(task['status']['errors'])
    # errors = [r['errors'] for r in task_results.copy()]
    print('\ntask result = {}, \n\nerrors : {}'.format(task_results_successful.copy(), errors))
    # if task_results == []:
    #   print('No email to be sent because no diff found.')
    # else:
    if mails is None:
        print('----> DIFF_END_ROUTINE <---- \n(RET = {})\n-----> No mail to be send .....'\
        .format(task_results))
    else:
        print('----> DIFF_END_ROUTINE <---- \n(RET = {})\n-----> Sending mail with diff template now .....'\
        .format(task_results))
        print("DIFF WITH KEYWORDS MAILS TEMPLATE CONTENT : {}".format(mails))
        #simple_mail_sbb(task_results, "simon.sicard@gmail.com")
        generic_mail_template(task_results_successful, errors, mails, 'diff task', len(task_results), show_links=True)
        print('- Mails successfully sent if any changed noticed -')
    print("DIFF MAILS TEMPLATE CONTENT : {}".format(mails))
    
    # Updating and download content now ...
    urls = [x['url'] for x in task_results_successful]
    make_request_for_updating_content(user_email, project_name, urls)
    print('All links ({}) successfully updated ! Yeay ! :)) '.format([x['url'] for x in task_results_successful]))

@app.task(bind=True)
def diff_task(self, add, mails, user_email, project_name):
    #print('ARGS SENT ==> {}'.format([[k[0], k[1], k[2], k[3]] for k in add]))
    return (group(get_diff.s(k[0], k[1], k[2], k[3], k[4], k[5], k[6]) for k in add) | diff_with_keywords_end_routine.s(mails, user_email, project_name)).delay()
    # return celery.chord((get_diff.s(k[0], k[1], k[2], k[3], k[4], k[5], k[6]\
    #     ).on_error(log_error_diff.s()) for k in add), diff_end_routine.s(mails, user_email, project_name))()

###################################################################################################



############################### DIFF WITH KEYWORDS SCHEDULED ROUTINE ##############################
@app.task(bind=True)
# def log_error_diff_with_keywords(request):
#     print('Task {0} raised :/'.format(request))
def log_error_diff_with_keywords(self, z):
    print('---> Error With Task <---')
    #print('ERROR for diff_with_keywords_task = {} [{}] -> (traceback = {})'.format(z, self.__dict__, self.__trace__.__dict__))

@app.task(bind=True)
def bad_task(self):
    time.sleep(10)

@app.task(bind=True)
def diff_with_keywords_end_routine(self, task_results, mails, user_email, project_name):#, soft_time_limit=120):
    print('----> DIFF_WITH_KEYWORDS_END_ROUTINE <---- \n(RET = {})\n----->\
     Sending mail with diff template now .....'\
        .format(task_results))
    errors = dict()
    if isinstance(task_results, dict):
        if task_results['status']['diff_pos'] != [] or task_results['status']['diff_neg'] != []:
            task_results_successful = [task_results['status']]
        else:
            task_results_successful = []
        errors.update(task_results['status']['errors'])
    else:
        task_results_successful = [r['status'] for r in task_results if (r['status']['diff_neg'] != []\
                     or r['status']['diff_pos'] != [])]
        for task in task_results.copy():
            if task['status']['errors'] != {}:
                errors.update(task['status']['errors'])
    # errors = [r['errors'] for r in task_results.copy()]
    print('\ntask result = {}, \n\nerrors : {}'.format(task_results_successful.copy(), errors))
    # if task_results == []:
    #   print('No email to be sent because no diff found.')
    # else:
    if mails is None:
        print('----> DIFF_END_ROUTINE <---- \n(RET = {})\n-----> No mail to be send .....'\
        .format(task_results))
    else:
        print('----> DIFF_END_ROUTINE <---- \n(RET = {})\n-----> Sending mail with diff with keywords template now .....'\
        .format(task_results))
        print("DIFF WITH KEYWORDS MAILS TEMPLATE CONTENT : {}".format(mails))
        #simple_mail_sbb(task_results, "simon.sicard@gmail.com")
        generic_mail_template(task_results_successful, errors, mails, 'diff with keywords task', len(task_results), show_links=True)
        print('- Mails successfully sent if any changed noticed -')
    print("DIFF WITH KEYWORDS MAILS TEMPLATE CONTENT : {}".format(mails))
    
    # Updating and download content now ...
    if task_results_successful != []:
        urls = [x['url'] for x in task_results_successful if (x['errors'] == {} and (x['diff_neg'] != [] or x['diff_pos'] != []))]
        make_request_for_updating_content(user_email, project_name, urls)
        print('All links ({}) successfully updated ! Yeay ! :)) '.format([x['url'] for x in task_results_successful]))
        
@app.task(bind=True)
def diff_with_keywords_task(self, add, mails, user_email, project_name):
    # print('ARGS SENT ==> {}'.format([[k[0], k[1], k[2], k[3]] for k in add]))
    # return celery.chord(
    #     (get_diff.s(k[0], k[1], k[2], k[3], k[4], k[5], k[6]) for k in add), 
    #     diff_with_keywords_end_routine.s(mails, user_email, project_name)
    # )()
    print('ADD = {}'.format(add))
    print('len ADD = {}'.format(len(add)))
    if len(add) == 1:
        return (get_diff.s(add[0][0], add[0][1], add[0][2], add[0][3], add[0][4], add[0][5], add[0][6]) | diff_with_keywords_end_routine.s(mails, user_email, project_name)).delay()
    # return (group(get_diff.s(k[0], k[1], k[2], k[3], k[4], k[5], k[6]) for k in add) | bad_task() | diff_with_keywords_end_routine.s(mails, user_email, project_name)).delay()
    else:
        return (group(get_diff.s(k[0], k[1], k[2], k[3], k[4], k[5], k[6]) for k in add) | diff_with_keywords_end_routine.s(mails, user_email, project_name)).delay()
    # return celery.chord(get_diff.s(k[0], k[1], k[2], k[3], k[4], k[5], k[6]\
        # ) for k in add | diff_with_keywords_end_routine.s(mails, \
    # user_email, project_name).on_error(log_error_diff_with_keywords.s()))
    # return res.get()

###################################################################################################
