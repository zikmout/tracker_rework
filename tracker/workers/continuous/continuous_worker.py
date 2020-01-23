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
from tracker.mail import generic_mail_template#, sbb_mail_template
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
        http_client.close()
        return response.body
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
        http_client.close()
        return response.body
    # except httpclient.HTTPError as e:
    #     print('HTTPError -> {}'.format(e))
    #     http_client.close()
    except Exception as e:
        print('Error -> {}'.format(e))
        http_client.close()
        return json.dumps({ 'error': '{}'.format(e)})

def is_sbb_content(url, language='ENGLISH', min_acc=0.8):
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
        # print('** {} has been redirected to : {} **'.format(response.geturl(), url))
        url = response.geturl()
        if url in already_visited:
            return False
        already_visited.append(url)

    filename = url.rpartition('/')[2]

    # get header charset
    info = response.info()
    cs = info.get_content_type()

    try:
        if extractor.is_valid_file(filename) or 'pdf' in cs:
            # print('URL = {} (detected pdf)'.format(url))
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
            # print('URL = {} (detected NON pdf)'.format(url))
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
    except Exception as e:
        return { 'error': '{}'.format(e)}
    return False

def get_full_links(status, base_url):
    keys = ['all_links_pos', 'all_links_neg']
    for _ in keys:
        if status[_] != []:
            idx = 0
            for x in status[_]:
                #print('log status {}. x = {}'.format(_, x))
                if x.startswith(base_url) is False:
                    if x.startswith('//'):
                        status[_][idx] = 'http:' + x
                    elif x.startswith('http') is False:
                        status[_][idx] = base_url + x
                    # else:
                    #     status[_][idx] = x
                idx += 1

    keys = ['nearest_link_pos', 'nearest_link_neg']
    for _ in keys:
        for k, v in status[_].copy().items():
            if v.startswith(base_url) is False:
                if v.startswith('http') is False:
                    status[_][k] = base_url + v
                # else
    #print('RETURNED ALL LINKS POS = {} (len = {})'.format(status['all_links_pos'], len(status['all_links_pos'])))
    return status

@app.task(bind=True)
def bad_task(self):
    print('start bad task')
    time.sleep(10)
    print('stop sleep')

@app.task(bind=True, ignore_result=False, soft_time_limit=50, time_limit=50)#soft_time_limit=60)#, time_limit=121)
def get_diff(self, link, base_path, diff_path, url, keywords_diff, detect_links, show_links,\
    links_algorithm, counter, total_task):
    """ Download website parts that have changed 
        -> diff based on keyword matching
        -> links identified with ml algorithm that detect share buy back content (pdf or raw text)
    """
    # VAL = [['/en/investors/stock-and-shareholder-corner/buyback-programs', ['DAILY DETAILS FOR THE PERIOD']]]
    # trying to hide scrapping patterns
    # random.shuffle(links)
    # total = len(links)
    # i = 0
    # print('before task. sleeping now. self = {}'.format(self.__dict__))
    # time.sleep(random.randint(0, 10))
    # print('after task')
    # print('LINKS ------> {}'.format(links))
    # print('base_path ------> {}'.format(base_path))
    # print('diff_path ------> {}'.format(diff_path))
    # print('url ------> {}'.format(url))
    # for link in links:
    keywords = link[1] if keywords_diff else []
    link = link[0]
    flink = url + utils.find_internal_link(link)
    # i += 1
    status = {
        'url': flink,
        'div': url.split('//')[-1].split('/')[0],
        'diff_neg': list(),
        'diff_pos': list(),
        'nearest_link_pos': dict(),
        'nearest_link_neg': dict(),
        'all_links_pos': list(),
        'all_links_neg': list(),
        'sbb_links_pos': list(),
        'sbb_links_neg': list(),
        'diff_nb': 0,
        'errors': dict(),
        'keywords': list()
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

        if remote_content is None:
            print('!!!! Problem fetching remote content. !!!! ERROR = {}'.format(error_remote_content))
            status['errors'].update(error_remote_content)

        if local_content is None:
            print('!!!! Problem fetching local content !!!! (url:{})'.format(flink))
            print('Downloading page : {} now ....'.format(flink))
            
            name = link.rpartition('/')[2]
            base_path = link.rpartition('/')[0]
            # dir_path = os.path.join(base_dir_path_file, 'website_content', utils.find_internal_link(flink).rpartition('/')[0][1:])
            print('base dir path = {}, website_content, internal link = {}'.format(base_dir_path, utils.find_internal_link(flink).rpartition('/')[0][1:]))
            #header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
            #print('--- [PARAMS] ---> flink : {}, name : {}, base_dir_path_file : {}'.format(flink, name, base_dir_path))

            res = False
            if remote_content is not None:
                res = downloader.save_remote_content(remote_content, url, base_dir_path, filename)
            if res:
                status['errors'].update({url: 'Page sucessfully downloaded'})
        
        if remote_content is not None and local_content is not None:
            if isinstance(remote_content, bytes):
                remote_content = remote_content.decode('utf-8', errors='ignore').replace('<b>', '').replace('</b>', '')
            if isinstance(local_content, bytes):
                local_content = local_content.decode('utf-8', errors='ignore').replace('<b>', '').replace('</b>', '')
            
            status = extractor.get_text_diff(local_content, remote_content, status,\
                detect_links=show_links)
            # if a list of keywords is provided, only get diff that matches keywords
            if keywords != [] and not isinstance(keywords[0], float):
                print('Keywords arrived like THIS = {}'.format(keywords))
                # Put keywords in status in order to highlight them on front side
                
                if isinstance(keywords, list) and isinstance(keywords[0], str):
                    if ';' in keywords[0]:
                        for _ in keywords[0].split(';'):
                            status['keywords'].append(_)
                    else:
                        status['keywords'] = keywords;
                # if len(keywords) == 1 and:
                    # status['keywords'] = keywords
                status = extractor.keyword_match(keywords, status, local_content, remote_content, url,\
                    detect_links=show_links)
                # Add update for status keywords
                self.update_state(state='PROGRESS', meta={'url': flink, 'current': counter, 'total': total_task, 'status': status})

            # else get nearest link for each diff
            elif keywords == []:
                extractor.nearest_link_match(status, local_content, remote_content, url)
            #print('******* len status all linsk pos 1: {}'.format(len(status['all_links_pos'])))
            # if detect_links:
                    
            #print('******* len status all linsk pos 2: {}'.format(len(status['all_links_pos'])))
            status = get_full_links(status, url)
            if detect_links:
            # status = select_only_sbb_links(status, show_links=show_links)
                for _ in status['all_links_pos'].copy():

                    res = is_sbb_content(_)
                    # print('RES = {} TYPE = {}'.format(res, type(res)))
                    if isinstance(res, bool) and res is True:
                        print('RES IS TRUE POS ---------->  {}'.format(_))
                        status['sbb_links_pos'].append(_)
                        self.update_state(state='PROGRESS', meta={'url': flink, 'current': counter, 'total': total_task, 'status': status})
                    # elif isinstance(res, dict):
                        # status['errors'].update({status['url'] : '{}'.format(res['error'])})
                        # self.update_state(state='PROGRESS', meta={'url': flink, 'current': counter, 'total': total_task, 'status': status})


                    # if isinstance(res, dict):#res and 'error' in res:
                       # status['errors'].update({status['url'] : '{}'.format(res['error'])})
                    # elif res 

                       # self.update_state(state='PROGRESS', meta={'url': flink, 'current': counter, 'total': total_task, 'status': status})
                    # else:
                    #     continue

                for _ in status['all_links_neg'].copy():
                    res = is_sbb_content(_)
                    # print('RES = {} TYPE = {}'.format(res, type(res)))
                    if isinstance(res, bool) and res is True:
                        print('RES IS TRUE NEG ---------->  {}'.format(_))
                        status['sbb_links_neg'].append(_)
                        self.update_state(state='PROGRESS', meta={'url': flink, 'current': counter, 'total': total_task, 'status': status})

            #print('******* len status all linsk pos 3: {}'.format(len(status['all_links_pos'])))
            self.update_state(state='PROGRESS', meta={'url': flink, 'current': counter, 'total': total_task, 'status': status})
            
            #print('\n\n ({}) DIFF POS:\n{}'.format(url, status['diff_pos']))
            #print('\n\n ({}) DIFF NEG :\n{}'.format(url, status['diff_neg']))
            if len(status['diff_pos']) > 0 or len(status['diff_neg']) > 0:
                print('***** Content is DIFFERENT ({}) *****'.format(flink))
                status['diff_nb'] += 1
            else:
                #print('***** Content is SIMILAR *****')
                pass
        return {'current': 100, 'total': 100, 'status': status, 'result': status['diff_nb']}
    except Exception as e:
        # pass
        # status['diff_nb'] = 0
        print("Share buy back diff exception => {}".format(e))
        status['errors'].update({status['url'] : '{}'.format(e)})
        self.update_state(state='PROGRESS', meta={'url': flink, 'current': counter, 'total': total_task, 'status': status})
        return {'url': flink, 'current': counter, 'total': total_task, 'status': status, 'result': status['diff_nb']}

    return {'url': flink, 'current': counter, 'total': total_task, 'status': status, 'result': status['diff_nb']}


###################################### SBB SCHEDULED ROUTINE ######################################
@app.task(bind=True)
def log_error_sbb(self, z):
    print('ERROR for share_buy_back_task = {}'.format(z))

@app.task(bind=True)
def sbb_end_routine(self, task_results, mails, user_email, project_name, show_links):#, soft_time_limit=120):
    errors = dict()
    task_results_successful = []
    if isinstance(task_results, dict):
        if task_results['status']['diff_pos'] != [] or task_results['status']['diff_neg'] != []:
            task_results_successful = [task_results['status']]
        errors.update(task_results['status']['errors'])
    else:
        for _ in task_results:
            # try:
            if 'status' in _ and (_['status']['diff_neg'] != [] or _['status']['diff_pos'] != []):
                task_results_successful.append(_['status'])
            if 'status' in _ and _['status']['errors'] != {}:
                errors.update(_['status']['errors'])
            # except Exception as e:
                # errors.update(_['status']['errors'])
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
        generic_mail_template(task_results_successful, errors, mails, 'sbb', len(task_results), show_links=show_links)
        print('- Mails successfully sent if any changed noticed -')
    print("SBB MAILS TEMPLATE CONTENT : {}".format(mails))
    
    # Updating and download content now ...
    urls = [x['url'] for x in task_results_successful]
    # make_request_for_updating_content(user_email, project_name, urls)
    print('All links ({}) successfully updated ! Yeay ! :)) '.format([x['url'] for x in task_results_successful]))

@app.task(bind=True)
def share_buy_back_task(self, add, mails, user_email, project_name, show_links):
    #print('ARGS SENT ==> {}'.format([[k[0], k[1], k[2], k[3]] for k in add]))
    #.set(
                # soft_time_limit=1
            # )
    if len(add) == 1:
        return (get_diff.s(add[0][0], add[0][1], add[0][2], add[0][3], add[0][4], add[0][5], add[0][6], add[0][7], add[0][8], add[0][9]) | sbb_end_routine.s(mails, user_email, project_name, show_links)).delay()
    else:
        return (group(get_diff.s(k[0], k[1], k[2], k[3], k[4], k[5], k[6], k[7], k[8], k[9]) for k in add) | sbb_end_routine.s(mails, user_email, project_name, show_links)).delay()
    # return celery.chord((get_diff.s(k[0], k[1], k[2], k[3], k[4], k[5], k[6]\
    #     ).on_error(log_error_sbb.s()) for k in add), sbb_end_routine.s(mails, user_email, project_name))()
    # return celery.chord((get_diff.s(k[0], k[1], k[2], k[3], k[4], k[5], k[6]\
        # ).set(soft_time_limit=500) for k in add), sbb_end_routine.s(mails, user_email, project_name))()

###################################################################################################



###################################### DIFF SCHEDULED ROUTINE #####################################
@app.task(bind=True)
def log_error_diff(self, z):
    print('ERROR for diff_task = {}'.format(z))

@app.task(bind=True)
def diff_end_routine(self, task_results, mails, user_email, project_name, show_links):#, time_limit=10, soft_time_limit=10):#, soft_time_limit=120):
    errors = dict()
    task_results_successful = []
    if isinstance(task_results, dict):
        if task_results['status']['diff_pos'] != [] or task_results['status']['diff_neg'] != []:
            task_results_successful = [task_results['status']]
        errors.update(task_results['status']['errors'])
    else:
        for _ in task_results:
            # try:
            if 'status' in _ and (_['status']['diff_neg'] != [] or _['status']['diff_pos'] != []):
                task_results_successful.append(_['status'])
            if 'status' in _ and _['status']['errors'] != {}:
                errors.update(_['status']['errors'])
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
        print("DIFF MAILS TEMPLATE CONTENT : {}".format(mails))
        #simple_mail_sbb(task_results, "simon.sicard@gmail.com")
        generic_mail_template(task_results_successful, errors, mails, 'diff', len(task_results), show_links=show_links)
        print('- Mails successfully sent if any changed noticed -')
    print("DIFF MAILS TEMPLATE CONTENT : {}".format(mails))
    
    # Updating and download content now ...
    urls = [x['url'] for x in task_results_successful]
    # make_request_for_updating_content(user_email, project_name, urls)
    print('All links ({}) successfully updated ! Yeay ! :)) '.format([x['url'] for x in task_results_successful]))

@app.task(bind=True)
def diff_task(self, add, mails, user_email, project_name, show_links):
    #print('ARGS SENT ==> {}'.format([[k[0], k[1], k[2], k[3]] for k in add]))
    if len(add) == 1:
        return (get_diff.s(add[0][0], add[0][1], add[0][2], add[0][3], add[0][4], add[0][5], add[0][6], add[0][7], add[0][8], add[0][9]) | diff_end_routine.s(mails, user_email, project_name, show_links)).delay()
    else:
        return (group(get_diff.s(k[0], k[1], k[2], k[3], k[4], k[5], k[6], k[7], k[8], k[9]) for k in add) | diff_end_routine.s(mails, user_email, project_name, show_links)).delay()
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
def diff_with_keywords_end_routine(self, task_results, mails, user_email, project_name, show_links):#, soft_time_limit=120):
    print('----> DIFF_WITH_KEYWORDS_END_ROUTINE <---- \n(RET = {})\n----->\
     Sending mail with diff template now .....'\
        .format(task_results))
    errors = dict()
    task_results_successful = []
    if isinstance(task_results, dict):
        if task_results['status']['diff_pos'] != [] or task_results['status']['diff_neg'] != []:
            task_results_successful = [task_results['status']]
        errors.update(task_results['status']['errors'])
    else:
        for _ in task_results:
            try:
                if _['status']['diff_neg'] != [] or _['status']['diff_pos'] != []:
                    task_results_successful.append(_['status'])
                if _['status']['errors'] != {}:
                    errors.update(_['status']['errors'])
            except Exception as e:
                errors.update(_['status']['errors'])

        # task_results_successful = [r['status'] for r in task_results if (r['status']['diff_neg'] != []\
        #              or r['status']['diff_pos'] != [])]
        # for task in task_results.copy():
        #     if task['status']['errors'] != {}:
        #         errors.update(task['status']['errors'])
    # errors = [r['errors'] for r in task_results.copy()]
    print('\ntask result successful = {}, \n\nerrors : {}'.format(task_results_successful, errors))
    # if task_results == []:
    #   print('No email to be sent because no diff found.')
    # else:
    if mails is None:
        print('----> DIFF_WITH_KEYWORDS_END_ROUTINE <---- \n(RET = {})\n-----> No mail to be send .....'\
        .format(task_results_successful))
    else:
        print('----> DIFF_WITH°KEYWORDS_END_ROUTINE <---- \n(RET = {})\n-----> Sending mail with diff with keywords template now .....'\
        .format(task_results_successful))
        print("DIFF WITH KEYWORDS MAILS TEMPLATE CONTENT : {}".format(mails))
        #simple_mail_sbb(task_results, "simon.sicard@gmail.com")
        generic_mail_template(task_results_successful, errors, mails, 'diff with keywords', len(task_results), show_links=show_links)
        print('- Mails successfully sent if any changed noticed -')
    print("DIFF WITH KEYWORDS MAILS TEMPLATE CONTENT : {}".format(mails))
    
    # Updating and download content now ...
    if task_results_successful != []:
        urls = [x['url'] for x in task_results_successful if (x['errors'] == {} and (x['diff_neg'] != [] or x['diff_pos'] != []))]
        # make_request_for_updating_content(user_email, project_name, urls)
        print('All links ({}) successfully updated ! Yeay ! :)) '.format([x['url'] for x in task_results_successful]))
        
@app.task(bind=True)
def diff_with_keywords_task(self, add, mails, user_email, project_name, show_links):
    # print('ARGS SENT ==> {}'.format([[k[0], k[1], k[2], k[3]] for k in add]))
    # return celery.chord(
    #     (get_diff.s(k[0], k[1], k[2], k[3], k[4], k[5], k[6]) for k in add), 
    #     diff_with_keywords_end_routine.s(mails, user_email, project_name)
    # )()
    print('ADD = {}'.format(add))
    print('len ADD = {}'.format(len(add)))
    if len(add) == 1:
        return (get_diff.s(add[0][0], add[0][1], add[0][2], add[0][3], add[0][4], add[0][5], add[0][6], add[0][7], add[0][8], add[0][9]) | diff_with_keywords_end_routine.s(mails, user_email, project_name, show_links)).delay()
    # return (group(get_diff.s(k[0], k[1], k[2], k[3], k[4], k[5], k[6]) for k in add) | bad_task() | diff_with_keywords_end_routine.s(mails, user_email, project_name)).delay()
    else:
        return (group(get_diff.s(k[0], k[1], k[2], k[3], k[4], k[5], k[6], k[7], k[8], k[9]) for k in add) | diff_with_keywords_end_routine.s(mails, user_email, project_name, show_links)).delay()
    # return celery.chord(get_diff.s(k[0], k[1], k[2], k[3], k[4], k[5], k[6]\
        # ) for k in add | diff_with_keywords_end_routine.s(mails, \
    # user_email, project_name).on_error(log_error_diff_with_keywords.s()))
    # return res.get()

###################################################################################################
