import os
import time
import random
import celery
import urllib
import ssl
from celery import Celery
from tracker.celery import app_socket
import tracker.core.utils as utils
import tracker.core.scrapper as scrapper
import tracker.core.extractor as extractor
import cld2
import re
import string
import pdftotext
import gc

import subprocess
from subprocess import check_output

def clean_pdf_content(input_str):
    print('-> cleaning pdf content ...')
    if input_str is None:
        return None
    #intput_str = ''.join(x for x in input_str if x.isprintable())
    input_str = ''.join(input_str).lower()
    output = re.sub(r'[0-9]', '', input_str)
    t = str.maketrans('', '', string.punctuation)
    output = output.translate(t)
    output = ' '.join(output.split())
    return output

def is_language(content, language):
    isReliable, textBytesFound, details = cld2.detect(content)
    if isReliable is True and details[0].language_name == language:
        return True
    return False

def is_valid_file(fname):
    to_include = ['.pdf', '.PDF']
    for _ in to_include:
        if _ in fname :
            return True
    if fname.startswith('.'):
        return False
    return False

def is_sbb_content(url, language='ENGLISH'):
    try:
        print('ENTER CHECK SBB : {}'.format(url))
        filename = url.rpartition('/')[2]
        if is_valid_file(filename):

            filename = url.rpartition('/')[2]
            req = urllib.request.Request(
                    url,
                    data=None,
                    headers=utils.rh()
            )
            # Faking SSL certificate to avoid unauthorized requests
            gcontext = ssl._create_unverified_context()
            print('FETCH URL: {}'.format(url))
            response = urllib.request.urlopen(req, context=gcontext)

            #info = response.info()
            #cs = info.get_content_type()
            #if 'pdf' in cs:


            cleaned_content = clean_pdf_content(pdftotext.PDF(response))
            print('cleaned content url {} = {}'.format(url, cleaned_content[:50]))
            if cleaned_content is None:
                print('Content {} is None !!!!!!!!!'.format(url))
                return False
            #if not is_language(cleaned_content, language):
            #    print('Language is NOT ENGLISH !!')
            #    return False
            with open(filename + '.txt', 'w+') as fd:
                print('creating file : {}'.format(filename))
                fd.write(cleaned_content)

            out = check_output(['./fasttext', 'predict-prob', 'model2.bin', filename + '.txt'])
            os.remove(filename + '.txt')
            print('-> deleted file : {}'.format(filename + '.txt'))
            #predictions = su_model.predict(cleaned_content)
            decoded = out.decode('utf-8')
            print('decoded = {}'.format(decoded))
            accuracy = float(decoded.split(' ')[1])
            if '__label__1' in decoded and accuracy > 0.9:
                prediction = '__label__1'
                print('Successfuly predicted \'{}\' with {} accuracy'.format(prediction, accuracy))
                return True
            else:
                prediction = '__label__2'
                print('Successfuly predicted \'{}\' with {} accuracy'.format(prediction, accuracy))
                return False
        else:
            return False
    except Exception as e:
        print('ERROR ************* : {} (link: {})'.format(e, url))
        return False
    return False

def select_only_sbb_links(status):
    print('\n-------------------------------———\n')
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
    print('RETURNED ALL LINKS POS = {} (len = {})'.format(status['all_links_pos'], len(status['all_links_pos'])))
    '''
    #select_only_sbb_links(status)
    for link in status['all_links_pos']:
        print('in list : {}'.format(link))
    for link in status['all_links_pos'].copy():
        print('in list 2 ======= {}'.format(link))
        try:
            print('TRYING LINK: {}'.format(link))
            if is_sbb_content(link) is False:
                print('pass link = {}'.format(link))
                status['all_links_pos'].remove(link)
            else:
                print('-------->>>>>>>>>>>>>< SBB not false')
        except:
            print('EOOR with link = {}'.format(link))
    '''
    return status

@app_socket.task(bind=True, ignore_result=False)
def live_view(self, links, base_path, diff_path, url):
    """ Try to download website parts that have changed """
    # VAL = [['/en/investors/stock-and-shareholder-corner/buyback-programs', ['DAILY DETAILS FOR THE PERIOD']]]
    #random.shuffle(links)
    total = len(links)
    i = 0
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
            print('******* len status all linsk pos 3: {}'.format(len(status['all_links_pos'])))
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