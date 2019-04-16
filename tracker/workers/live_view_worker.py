import os
import time
import random
import celery
import urllib
import ssl
from celery import Celery
from tracker.celery import app_socket
from celery.contrib.abortable import AbortableTask
import tracker.core.utils as utils
import tracker.core.scrapper as scrapper
import tracker.core.extractor as extractor
import cld2
import re
import string
import pdftotext
import gc
import fastText

global su_model

import tracker.ml_toolbox as mltx

su_model = mltx.SU_Model('trained_800_wiki2.bin').su_model

def clean_content(input_list, min_sentence_len=5):
    print('-> cleaning HTML content ....')
    """ Method that clean every element of a list
        arg:
            input_list(list): List of elements to be cleaned
        return:
            ouput (list): List of cleaned elements
    """
    if input_list is None:
        return None
    output = [x for x in input_list if x != '\n']
    output = [x for x in output if len(x.split(' ')) > min_sentence_len]

    # to lower
    output = [x.lower() for x in output]
    
    # get rid of punctuation
    t = str.maketrans('', '', string.punctuation)
    output = [x.translate(t) for x in output]
    
    # get rid of digits
    t = str.maketrans('', '', string.digits)
    output = [x.translate(t) for x in output]
    
    # get rid of whitespaces
    t = str.maketrans('\n\t\r', '   ')
    output = [x.translate(t) for x in output]
    
    # get rid of cookie and javascript sentences
    to_exclude = ['cookie', 'javascript']
    for _ in to_exclude:
        output = [x for x in output if _ not in x]
    
    return output

def get_essential_content(content, min_sentence_len):
    extracted = extractor.extract_text_from_html(content)
    cleaned = clean_content(extracted, min_sentence_len)
    cleaned = list(map(str.strip, cleaned))
    cleaned = [x for x in cleaned if len(x.split(' ')) > min_sentence_len]
    cleaned = ''.join(cleaned)
    if cleaned == '':
        return None
    else:
        return cleaned

def clean_pdf_content(input_str):
    print('-> cleaning pdf content ...')
    if input_str is None:
        return None
    intput_str = ''.join(x for x in input_str if x.isprintable())
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

def make_predictions(content, min_acc=0.75):
    global su_model
    #print('su_model : {}'.format(su_model))
    #gc.collect()
    print('content : {} [...]'.format(content[:100]))
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
    filename = url.rpartition('/')[2]

    # get header charset
    info = response.info()
    cs = info.get_content_type()

    if is_valid_file(filename) or 'pdf' in cs:
        #print('URL = {} (detected pdf)'.format(url))
        cleaned_content = clean_pdf_content(pdftotext.PDF(response))
        #print('cleaned content url {} = {}'.format(url, cleaned_content[:50]))
        if cleaned_content is None:
            #print('Content {} is None !!!!!!!!!'.format(url))
            return False
        # if not is_language(cleaned_content, 'ENGLISH'):
        #     print('Language is NOT ENGLISH !! (Content = {}...)'.format(cleaned_content[:100]))
        #     return False

        '''
        with open(filename + '.txt', 'w+') as fd:
            #print('creating file : {}'.format(filename))
            fd.write(cleaned_content)

        out = check_output(['./fasttext', 'predict-prob', 'model2.bin', filename + '.txt'])
        os.remove(filename + '.txt')
        #print('-> deleted file : {}'.format(filename + '.txt'))
        #predictions = su_model.predict(cleaned_content)
        decoded = out.decode('utf-8')
        print('decoded = {}'.format(decoded))
        accuracy = float(decoded.split(' ')[1])
        if '__label__1' in decoded and accuracy > 0.8:
            prediction = '__label__1'
            #print('Successfuly predicted \'{}\' with {} accuracy'.format(prediction, accuracy))
            return True
        else:
            prediction = '__label__2'
            #print('Successfuly predicted \'{}\' with {} accuracy'.format(prediction, accuracy))
            return False
        '''
        return make_predictions(cleaned_content, min_acc=min_acc)

    else:
        print('URL = {} (detected NON pdf)'.format(url))
        cleaned_content = get_essential_content(response.read(), 10)

        if cleaned_content is None:
            #print('Content {} is None !!!!!!!!!'.format(url))
            return False
        #content = extractor.extract_text_from_html(response.read())
        #cleaned_content = extractor.clean_content(content)
        #print('Content to analyse = {}'.format(cleaned_content[:100]))
        # if not is_language(cleaned_content, 'ENGLISH'):
        #     print('Language is NOT ENGLISH (non pdf) !! (Content = {}...)'.format(cleaned_content[:100]))
        #     return False
        #preds = mmodel.su_model.predict(cleaned_content, k=2)
        '''
        with open(filename + '.txt', 'w+') as fd:
            print('creating file : {}'.format(filename))
            fd.write(cleaned_content)

        out = check_output(['./fasttext', 'predict-prob', 'model2.bin', filename + '.txt'])
        os.remove(filename + '.txt')
        print('-> deleted file : {}'.format(filename + '.txt'))
        '''
        #predictions = su_model.predict(cleaned_content)
        return make_predictions(cleaned_content, min_acc=min_acc)
        '''
        decoded = out.decode('utf-8')
        print('decoded (non PDF) = {}'.format(decoded))
        accuracy = float(decoded.split(' ')[1])
        if '__label__1' in decoded and accuracy > 0.9:
            prediction = '__label__1'
            print('Successfuly predicted \'{}\' with {} accuracy (non PDF)'.format(prediction, accuracy))
            return True
        else:
            prediction = '__label__2'
            print('Successfuly predicted \'{}\' with {} accuracy (non PDF)'.format(prediction, accuracy))
            return False
            '''

        return False


    return False

def select_only_sbb_links(self, status):
    print('\n-------------------------------———\n')
    i = 0
    excluded_links = list()
    for link in status['all_links_pos'].copy():
        i += 1
        if not i % 5:
            if self.is_aborted():
                return False
        if is_sbb_content(link) is False:
            excluded_links.append(link)
            status['all_links_pos'].remove(link)#(index)
    for link in status['all_links_neg'].copy():
        i += 1
        if not i % 5:
            if self.is_aborted():
                return False
        if is_sbb_content(link) is False:
            excluded_links.append(link)
            status['all_links_neg'].remove(link)
    for link in status['nearest_link_pos'].copy():
        i += 1
        if not i % 5:
            if self.is_aborted():
                return False
        if is_sbb_content(link) is False:
            excluded_links.append(link)
            status['nearest_link_pos'].remove(link)
    for link in status['nearest_link_neg'].copy():
        i += 1
        if not i % 5:
            if self.is_aborted():
                return False
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

@app_socket.task(bind=True, base=AbortableTask, ignore_result=False, soft_time_limit=900)
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
            status = select_only_sbb_links(self, status)

            if status is False:
                print('\n-------- TASK ABORTED -------\n')
                return
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