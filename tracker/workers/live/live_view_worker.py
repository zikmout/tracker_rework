import os
import time
# import random
import celery
import urllib
import ssl
import json
from celery import Celery
from tornado import httpclient
from tracker.utils import format_all_nearest_links
from tracker.celery import live_view_worker_app
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
        # print('-- [ERROR FETCHING URL {}] --\nReason:{}\n'.format(url, e))
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

    try:
        if extractor.is_valid_file(filename) or 'pdf' in cs:
            #print('URL = {} (detected pdf)'.format(url))
            cleaned_content = extractor.clean_pdf_content(pdftotext.PDF(response))
            #print('cleaned content url {} = {}'.format(url, cleaned_content[:50]))
            if cleaned_content is None or cleaned_content in already_seen_content:
                #print('Content {} is None !!!!!!!!!'.format(url))
                return False
                # return { 'error': 'Content is none or has already been seen: ({})'.format(url)}
            already_seen_content.append(cleaned_content)
            # if not extractor.is_language(cleaned_content, 'ENGLISH'):
            #     print('Language is NOT ENGLISH !! (Content = {}...)'.format(cleaned_content[:100]))
            #     return False
            resp = make_request_for_predictions(cleaned_content, min_acc=min_acc)
            # print('response = {}'.format(resp))
            return json.loads(resp)

        else:
            # if 'www.facebook.' or 'www.twitter.' or 'www.youtube.' in url:
            #     return False
            print('URL = {} (detected NON pdf)'.format(url))
            cleaned_content = extractor.get_essential_content(response.read(), 10)

            if cleaned_content is None or cleaned_content in already_seen_content:
                #print('Content {} is None !!!!!!!!!'.format(url))
                # return { 'error': 'Content is none or has already been seen: ({})'.format(url)}
                return False
            already_seen_content.append(cleaned_content)
            #content = extractor.extract_text_from_html(response.read())
            #cleaned_content = extractor.clean_content(content)
            #print('Content to analyse = {}'.format(cleaned_content[:100]))
            # if not extractor.is_language(cleaned_content, 'ENGLISH'):
            #     print('Language is NOT ENGLISH (non pdf) !! (Content = {}...)'.format(cleaned_content[:100]))
            #     return False
            resp = make_request_for_predictions(cleaned_content, min_acc=min_acc)
            # print('response = {}'.format(resp))
            return json.loads(resp)
    except Exception as e:
        return { 'error': '{}'.format(e)}
    return False

def get_full_links(status, base_url):
    keys = ['all_links_pos', 'all_links_neg']
    for _ in keys:
        if status[_] != []:
            idx = 0
            for x in status[_].copy():
                if x.startswith(base_url) is False:
                    if x.startswith('//'):
                        status[_][idx] = 'http:' + x
                    elif x.startswith('http') is False:
                        status[_][idx] = base_url + x
                if x.startswith('/'):
                    status[_][idx] = base_url + x
                idx += 1

    keys = ['nearest_link_pos', 'nearest_link_neg']
    for _ in keys:
        for k, v in status[_].copy().items():
            if v.startswith(base_url) is False:
                if x.startswith('//'):
                    status[_][k] = 'http:' + v
                elif v.startswith('http') is False:
                    status[_][k] = base_url + v
            if x.startswith('/'):
                status[_][k] = base_url + v
    return status
    # status['nearest_link_neg'] = format_all_nearest_links(status['nearest_link_neg'], base_url)
    # status['nearest_link_pos'] = format_all_nearest_links(status['nearest_link_pos'], base_url)
    
    return status

@live_view_worker_app.task(bind=True, ignore_result=False, soft_time_limit=50)#, time_limit=5)
def live_view(self, link, base_path, diff_path, url, keywords_diff, detect_links,\
    show_links, links_algorithm, counter, total_task):
    """ Download website parts that have changed 
        -> diff based on keyword matching
        -> links identified with ml algorithm that detect share buy back content (pdf or raw text)
    """
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
        'all_nearest_links_local': dict(),
        'all_nearest_links_remote': dict(),
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
        # print('FILNAME = {}'.format(filename))
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
            if isinstance(remote_content, bytes):
                remote_content = remote_content.decode('utf-8', errors='ignore')
            remote_content = remote_content.replace('<b>', '').replace('</b>', '').replace('&nbsp;', ' ')
            status = extractor.get_nearest_link_with_bs(remote_content, status, 'all_nearest_links_remote')
                # print('NEAREST LINKKK LOCAL === {}'.format(status['all_nearest_links_local']))
            if isinstance(local_content, bytes):
                local_content = local_content.decode('utf-8', errors='ignore')
            local_content = local_content.replace('<b>', '').replace('</b>', '').replace('&nbsp;', ' ')
            status = extractor.get_nearest_link_with_bs(local_content, status, 'all_nearest_links_local')

            status = extractor.get_text_diff(local_content, remote_content, status,\
                detect_links=show_links)
            # if a list of keywords is provided, only get diff that matches keywords
            if keywords != [] and not isinstance(keywords[0], float):
                #print('Keywords arrived like THIS = {}'.format(keywords))
                # Put keywords in status in order to highlight them on front side
                
                if isinstance(keywords, list) and isinstance(keywords[0], str):
                    if ';' in keywords[0]:
                        for _ in keywords[0].split(';'):
                            status['keywords'].append(_)
                    else:
                        status['keywords'] = keywords;

                status = extractor.keyword_match(keywords, status, local_content, remote_content, url,\
                    detect_links=show_links)
                # Add update for status keywords
                self.update_state(state='PROGRESS', meta={'url': flink, 'current': counter, 'total': total_task, 'status': status})

            # else get nearest link for each diff
            elif keywords == []:
                # status = extractor.nearest_link_match(status, local_content, remote_content, url)
                status = extractor.nearest_link_match_bs(status, local_content, remote_content, url)

                #print('******* len status all linsk pos 1: {}'.format(len(status['all_links_pos'])))
                print('status nearest_link_neg = {}'.format(status['nearest_link_neg']))
                print('status nearest_link_pos = {}'.format(status['nearest_link_pos']))
                
            #print('******* len status all linsk pos 2: {}'.format(len(status['all_links_pos'])))
            
            # status['all_nearest_links_remote'] = format_all_nearest_links(status['all_nearest_links_remote'], url)
            # status['all_nearest_links_local'] = format_all_nearest_links(status['all_nearest_links_local'], url)
            
            if detect_links:
                # status = select_only_sbb_links(status, show_links=show_links)
                for _ in status['all_links_pos']:

                    res = is_sbb_content(_)
                    # print('RES = {} TYPE = {}'.format(res, type(res)))
                    if isinstance(res, bool) and res is True:
                        # print('RES IS TRUE POS ---------->  {}'.format(_))
                        status['sbb_links_pos'].append(_)
                        self.update_state(state='PROGRESS', meta={'url': flink, 'current': counter, 'total': total_task, 'status': status})
                    elif isinstance(res, dict):
                        status['errors'].update({status['url'] : '{}'.format(res['error'])})
                        self.update_state(state='PROGRESS', meta={'url': flink, 'current': counter, 'total': total_task, 'status': status})

                for _ in status['all_links_neg']:
                    res = is_sbb_content(_)
                    # print('RES = {} TYPE = {}'.format(res, type(res)))
                    if isinstance(res, bool) and res is True:
                        # print('RES IS TRUE NEG ---------->  {}'.format(_))
                        status['sbb_links_neg'].append(_)
                        self.update_state(state='PROGRESS', meta={'url': flink, 'current': counter, 'total': total_task, 'status': status})
                    elif isinstance(res, dict):
                        status['errors'].update({status['url'] : '{}'.format(res['error'])})
                        self.update_state(state='PROGRESS', meta={'url': flink, 'current': counter, 'total': total_task, 'status': status})
            
            status = get_full_links(status, url)
            print('AFTER STATUS GET FULL LINKS - nearest_link_neg = {}'.format(status['nearest_link_neg']))
            #print('******* len status all linsk pos 3: {}'.format(len(status['all_links_pos'])))
            self.update_state(state='PROGRESS', meta={'url': flink, 'current': counter, 'total': total_task, 'status': status})
            
            #print('\n\n ({}) DIFF POS:\n{}'.format(url, status['diff_pos']))
            #print('\n\n ({}) DIFF NEG :\n{}'.format(url, status['diff_neg']))
            if len(status['diff_pos']) > 0 or len(status['diff_neg']) > 0:
                print('***** Content is DIFFERENT ({}) *****'.format(flink))
                status['diff_nb'] += 1
            else:
                # print('***** Content is SIMILAR *****')
                pass
    except Exception as e:
        print("Share buy back diff exception => {}".format(e))
        status['errors'].update({status['url'] : '{}'.format(e)})
        self.update_state(state='PROGRESS', meta={'url': flink, 'current': counter, 'total': total_task, 'status': status})
        return {'url': flink, 'current': counter, 'total': total_task, 'status': status, 'result': status['diff_nb']}

    return {'url': flink, 'current': counter, 'total': total_task, 'status': status, 'result': status['diff_nb']}
