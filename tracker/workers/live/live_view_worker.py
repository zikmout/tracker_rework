import os
import time
# import random
import string
import celery
import urllib
import ssl
import json
from celery import Celery
from tracker.utils import format_all_nearest_links
from tracker.celery import live_view_worker_app
import tracker.core.utils as utils
import tracker.core.scrapper as scrapper
import tracker.core.extractor as extractor
import tracker.core.downloader as downloader
import tracker.core.predictor as predictor
from tracker.utils import trim_text
import re
import pdftotext
import gc
try:
    import fasttext as fastText
except:
    import fastText

already_visited = list()
already_seen_content = list()

def is_sbb_content(url, language='ENGLISH', min_acc=0.8):
    # time.sleep(2)
    if not utils.is_valid_url(url):
        return False

    req = urllib.request.Request(
            url,
            data=None,
            headers=utils.rh()
    )
    # Faking SSL certificate to avoid unauthorized requests
    gcontext = ssl._create_unverified_context()
    try:
        # if url == 'https://www.adidas-group.com/media/filer_public/e9/da/e9da3184-11ec-4d53-bd17-12780c95d469/en_publication_delvo_tranche_3_20200103.pdf':
        #     timeout = 60
        # else:
        #     timeout = 3
        response = urllib.request.urlopen(req, context=gcontext, timeout=12)
    except Exception as e:
        print('-- [ERROR FETCHING URL {}] --\nReason:{}\n'.format(url, e))
        return False

    if response.geturl() != url:
        print('## -> Redirection {} to : {} **'.format(response.geturl(), url))
        url = response.geturl()
        if url in already_visited:# or not is_valid_url(url):
            return False
        already_visited.append(url)

    filename = url.rpartition('/')[2]

    # get header charset
    info = response.info()
    cs = info.get_content_type()

    try:
        if extractor.is_valid_file(filename) or 'pdf' in cs:
            print('## Fetching : {} (detected pdf)'.format(url))
            cleaned_content = extractor.clean_pdf_content(pdftotext.PDF(response))
        else:
            print('## Fetching : {} (detected NON pdf)'.format(url))
            cleaned_content = extractor.get_essential_content(response.read(), 10)
            
        valid = utils.is_valid_cleaned_content(cleaned_content, already_seen_content)
        if not valid:
            return False
        already_seen_content.append(cleaned_content)
        # if not extractor.is_language(cleaned_content, 'ENGLISH'):
        #     return False
        resp = predictor.make_request_for_predictions(cleaned_content, min_acc=min_acc)
        return json.loads(resp)
    except Exception as e:
        return { 'error': '{}'.format(e)}
    return False

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
        'keywords': list(),
        'current_target' : list()
    }
    # try:
    if flink not in status['current_target']:
        status['current_target'].append(flink)
        self.update_state(state='PROGRESS', meta={'url': flink, 'current': counter, 'total': total_task, 'status': status})
    # print('[{}/{}] Link = {}'.format(i, len(links), flink))
    #time.sleep(random.randint(0, 10))
    base_dir_path = os.path.join(base_path, utils.find_internal_link(link).rpartition('/')[0][1:])
    filename = link.rpartition('/')[2]
    base_dir_path_file = os.path.join(base_dir_path, filename)

    # check whether adding 'unknown' is right ...
    if os.path.isdir(base_dir_path_file) and os.path.isfile(base_dir_path_file + 'unknown___'):
        base_dir_path_file = base_dir_path_file + 'unknown___'

    local_content = scrapper.get_local_content(base_dir_path_file, 'rb')
    remote_content, error_remote_content = scrapper.get_url_content(status['url'], header=utils.rh())

    if isinstance(remote_content, bytes):
        remote_content = remote_content.decode('utf-8', errors='ignore')

    if isinstance(local_content, bytes):
        local_content = local_content.decode('utf-8', errors='ignore')
    
    if remote_content is not None:
        remote_content = remote_content.replace('<b>', '').replace('</b>', '').replace('&nbsp;', ' ')
        # Next is supposed to be taken off slowly
    if local_content is not None:    
        local_content = local_content.replace('<b>', '').replace('</b>', '').replace('&nbsp;', ' ')

    if remote_content is None:
        # print('!!!! Problem fetching remote content. !!!! ERROR = {}'.format(error_remote_content))
        status['errors'].update(error_remote_content)
    
    if local_content is None:
        print('!!!! Problem fetching local content !!!! (url:{})'.format(flink))
        print('Downloading page : {} now ....'.format(flink))
        name = link.rpartition('/')[2]
        base_path = link.rpartition('/')[0]
        res = False
        if remote_content is not None:
            res = downloader.save_remote_content(remote_content, url, base_dir_path, filename)
        if res:
            status['errors'].update({url: 'Page sucessfully downloaded'})

        #err = downloader.download_and_save_content(flink, filename, base_dir_path, header, check_duplicates=False, replace=True)
        # TODO: Log errors from local content here and put in status just like for remote content

    if remote_content is not None and local_content is not None:
        
        status = extractor.get_nearest_link_with_bs(remote_content, status, 'all_nearest_links_remote')
        status = extractor.get_nearest_link_with_bs(local_content, status, 'all_nearest_links_local')

        
        # if a list of keywords is provided, only get diff that matches keywords
        if keywords != [] and not isinstance(keywords[0], float):
            # print('Keywords arrived like THIS = {}'.format(keywords))
            # Put keywords in status in order to highlight them on front side
            if isinstance(keywords, list) and isinstance(keywords[0], str):
                if ';' in keywords[0]:
                    for _ in keywords[0].split(';'):
                        status['keywords'].append(_)
                else:
                    status['keywords'] = keywords
        # TODO: send show_diff_pos and show_diff_neg to get_text_diff in order to avoir useless computation ?
        status = extractor.get_text_diff(local_content, remote_content, status, keywords_diff, keywords)#,\
            # detect_links=show_links)

        status = extractor.get_full_all_links(status, url)

        if status is None:
            return
            # status = extractor.keyword_match(keywords, status, local_content, remote_content, url)#,\
                # detect_links=show_links)

        # else get nearest link for each diff
        # elif keywords == [] and keywords_diff is False:
        status = extractor.nearest_link_match(status, local_content, remote_content, url)
        status = extractor.get_full_nearest_links(status, url)
        self.update_state(state='PROGRESS', meta={'url': flink, 'current': counter, 'total': total_task, 'status': status})

        # If asked to detect SBB links with ML algorithm
        if detect_links:
            # status = select_only_sbb_links(status, show_links=show_links)
            # print('ALL LINKS POS = {} '.format(status['all_links_pos']))
            for _ in status['all_links_pos']:
                # print('current + = {}'.format(_))
                if _ not in status['current_target']:
                    status['current_target'].append(_)
                self.update_state(state='PROGRESS', meta={'url': flink, 'current': counter, 'total': total_task, 'status': status})
                res = is_sbb_content(_)
                print('RES = {} TYPE = {}'.format(res, type(res)))
                if isinstance(res, bool) and res is True:
                    print('RES IS TRUE POS ---------->  {}'.format(_))
                    # status['current_target'] = {_:'sbb_links_pos'}
                    status['sbb_links_pos'].append(_)
                    self.update_state(state='PROGRESS', meta={'url': flink, 'current': counter, 'total': total_task, 'status': status})
                elif isinstance(res, dict):
                    status['errors'].update({status['url'] : '{}'.format(res['error'])})
                    self.update_state(state='PROGRESS', meta={'url': flink, 'current': counter, 'total': total_task, 'status': status})
                else:
                    # status['current_target'] = {_:'all_links_pos'}
                    self.update_state(state='PROGRESS', meta={'url': flink, 'current': counter, 'total': total_task, 'status': status})

            # print('ALL LINKS NEG = {} '.format(status['all_links_neg']))
            for _ in status['all_links_neg']:
                # print('current - = {}'.format(_))
                # status['current_target'] = {_:'all_links_neg'}
                if _ not in status['current_target']:
                    status['current_target'].append(_)
                self.update_state(state='PROGRESS', meta={'url': flink, 'current': counter, 'total': total_task, 'status': status})
                res = is_sbb_content(_)
                print('RES = {} TYPE = {}'.format(res, type(res)))
                if isinstance(res, bool) and res is True:
                    print('RES IS TRUE NEG ---------->  {}'.format(_))
                    # status['current_target'] = {_:'sbb_links_neg'}
                    status['sbb_links_neg'].append(_)
                    self.update_state(state='PROGRESS', meta={'url': flink, 'current': counter, 'total': total_task, 'status': status})
                elif isinstance(res, dict):
                    status['errors'].update({status['url'] : '{}'.format(res['error'])})
                    self.update_state(state='PROGRESS', meta={'url': flink, 'current': counter, 'total': total_task, 'status': status})
                else:
                    # status['current_target'] = {_:'all_links_neg'}
                    self.update_state(state='PROGRESS', meta={'url': flink, 'current': counter, 'total': total_task, 'status': status})

        self.update_state(state='PROGRESS', meta={'url': flink, 'current': counter, 'total': total_task, 'status': status})
        
        #print('\n\n ({}) DIFF POS:\n{}'.format(url, status['diff_pos']))
        #print('\n\n ({}) DIFF NEG :\n{}'.format(url, status['diff_neg']))
        if len(status['diff_pos']) > 0 or len(status['diff_neg']) > 0:
            print('***** Content is DIFFERENT ({}) *****'.format(flink))
            status['diff_nb'] += 1
        else:
            # print('***** Content is SIMILAR *****')
            pass
    # except Exception as e:
    #     print("Share buy back diff exception => {}".format(e))
    #     status['errors'].update({status['url'] : '{}'.format(e)})
    #     self.update_state(state='PROGRESS', meta={'url': flink, 'current': counter, 'total': total_task, 'status': status})
    #     return {'url': flink, 'current': counter, 'total': total_task, 'status': status, 'result': status['diff_nb']}

    return {'url': flink, 'current': counter, 'total': total_task, 'status': status, 'result': status['diff_nb']}
