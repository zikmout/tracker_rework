import os
import time
# import random
import celery
import urllib
import ssl
import json
from celery import Celery#, Task
from tornado import httpclient
from tracker.celery import live_view_worker_app
#from celery.contrib.abortable import AbortableTask
import tracker.core.utils as utils
import tracker.core.scrapper as scrapper
import tracker.core.extractor as extractor
import tracker.core.downloader as downloader

import re
import pdftotext
import gc
import fastText

already_visited = list()
already_seen_content = list()

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
        print('-- [ERROR FETCHING URL {}] --\nReason:{}\n'.format(url, e))
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
        resp = make_request_for_predictions(cleaned_content, min_acc=min_acc)
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
        return json.loads(resp)

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
                #print('log status {}. x = {}'.format(_, x))
                if x.startswith(base_url) is False:
                    if x.startswith('http') is False:
                        status[_][idx] = base_url + x
                    else:
                        status[_][idx] = x
                idx += 1
    print('RETURNED ALL LINKS POS = {} (len = {})'.format(status['all_links_pos'], len(status['all_links_pos'])))
    return status 

@live_view_worker_app.task(bind=True, ignore_result=False, soft_time_limit=50)#, time_limit=5)
def live_view(self, link, base_path, diff_path, url, keywords_diff, detect_links,\
    links_algorithm, counter, total_task):
    # if soft_time_limit is True:
        # self.soft_time_limit = soft_time_limit
    # print('SELF.TIMELIMIT = {}'.format(self.soft_time_limit))
    # try:
    """ Download website parts that have changed 
        -> diff based on keyword matching
        -> links identified with ml algorithm that detect share buy back content (pdf or raw text)
    """
    # VAL = [['/en/investors/stock-and-shareholder-corner/buyback-programs', ['DAILY DETAILS FOR THE PERIOD']]]
    # trying to hide scrapping patterns
    # random.shuffle(links)
    # total = len(links)
    # i = 0
    # # print('-> start task, sleeping.')
    # # time.sleep(6)
    # # print('-> stop sleeping.')
    # # print('LINKS ------> {}'.format(links))
    # # print('base_path ------> {}'.format(base_path))
    # # print('diff_path ------> {}'.format(diff_path))
    # # print('url ------> {}'.format(url))
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
        print('FILNAME = {}'.format(filename))
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

            #err = downloader.download_and_save_content(flink, filename, base_dir_path, header, check_duplicates=False, replace=True)
            # TODO: Log errors from local content here and put in status just like for remote content

        
        if remote_content is not None and local_content is not None:
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
            self.update_state(state='PROGRESS', meta={'url': flink, 'current': counter, 'total': total_task, 'status': status})
            
            #print('\n\n ({}) DIFF POS:\n{}'.format(url, status['diff_pos']))
            #print('\n\n ({}) DIFF NEG :\n{}'.format(url, status['diff_neg']))
            if len(status['diff_pos']) > 0 or len(status['diff_neg']) > 0:
                print('***** Content is DIFFERENT ({}) *****'.format(flink))
                status['diff_nb'] += 1
            else:
                print('***** Content is SIMILAR *****')
                pass
    except Exception as e:
        # TODO: Kill SIGKILL all pending tasks
        print("Share buy back diff exception => {}".format(e))
        status['errors'].update({status['url'] : '{}'.format(e)})
        return {'url': flink, 'current': counter, 'total': total_task, 'status': status, 'result': status['diff_nb']}

    return {'url': flink, 'current': counter, 'total': total_task, 'status': status, 'result': status['diff_nb']}
