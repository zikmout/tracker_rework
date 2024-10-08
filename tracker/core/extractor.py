import os
import http
import urllib
from urllib.request import urlopen
import ssl
import re
import html
# import cld2
import pycld2 as cld2
import string
from lxml.etree import tostring
from bs4 import BeautifulSoup
from bs4.element import Comment
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
from io import open
import lxml.html as LH
import itertools
import tracker.core.scrapper as scrapper
import tracker.core.utils as utils
from tracker.utils import trim_text

def clean_sentence(input_sentence):
        # to lower
        output = input_sentence.lower()
        output = output.replace('\n', '')\
        .replace('\r', '')\
        .replace('\t', '')\
        .replace(',', ' ')\
        .replace('  ', ' ')\
        .replace('-', ' ')
        return output

def clean_pdf_content(input_str):
    #print('-> cleaning pdf content ...')
    try:
        if input_str is None:
            return None
        # input_str = ''.join(x for x in input_str if x.isprintable())
        input_str = ''.join(input_str).lower()
        output = re.sub(r'[0-9]', '', input_str)
        t = str.maketrans('', '', string.punctuation)
        output = output.translate(t)
        output = ' '.join(output.split())
        return output
    except Exception as e:
        print('[CLEAN PDF CONTENT EXCEPTION] : {}'.format(e))
        return None

def clean_content(input_list, min_sentence_len=5):
    #print('-> cleaning HTML content ....')
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
    filters = ''.join([chr(i) for i in range(1, 32)])
    ouput = [_.translate(str.maketrans('', '', filters)).strip() for _ in output]
    
    # TODO: Add function to delete '-'s

    # get rid of cookie and javascript sentences
    # TODO: Use python built-in function filter here (https://www.w3schools.com/python/ref_func_filter.asp)
    to_exclude = ['cookie', 'javascript']
    for _ in to_exclude:
        output = [x for x in output if _ not in x]
    
    return output

def roundrobin(*iterables):
    # print('Enter roundrobin ALGO1:')
    # took from here https://docs.python.org/3/library/itertools.html#itertools-recipes

    """roundrobin('ABC', 'D', 'EF') --> A D E B F C"""
    # Recipe credited to George Sakkis

    pending = len(iterables)
    nexts = itertools.cycle(iter(it).__next__ for it in iterables)
    while pending:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            pending -= 1
            nexts = itertools.cycle(itertools.islice(nexts, pending))

def find_nearest(elt):
    # TODO: Take off links with '#' like adidas group
    preceding = elt.xpath('preceding::*/@href')[::-1]
    following = elt.xpath('following::*/@href')
    parent = elt.xpath('parent::*/@href')

    for href in roundrobin(parent, preceding, following):
        return href

def get_nearest_link(match, keyword, content):

    nearest_link = None
    # print('looking for kw ========> {}'.format(match))
    doc = LH.fromstring(content.replace('\'', ' '))
    try:
        el2 = doc.xpath('/html/body//a[contains(text(),{s!r})]/@href'.format(s = match))
    except Exception as e:
        return None
    if el2 != []:
        if '#' not in el2[0] and (el2[0].startswith('/') or el2[0].startswith('http')):
            return el2[0]
    else:
        for x in doc.xpath('//*[contains(text(),{s!r})]'.format(s = match)):
            nearest = find_nearest(x)
            if nearest is not None and '#' not in nearest and (nearest.startswith('/') or nearest.startswith('http')):
                nearest_link = nearest
                return nearest
    return nearest_link

def nearest_link_match(status, local_content, remote_content, url):
    for neg in status['diff_neg']:
        for k, v in status['all_nearest_links_local'].items():
            if neg in k:
                status['nearest_link_neg'][neg] = v
        if neg not in status['nearest_link_neg']:
            nearest = get_nearest_link(neg, neg, local_content)
            if nearest is not None:
                status['nearest_link_pos'][neg] = nearest

    for pos in status['diff_pos']:
        for k, v in status['all_nearest_links_remote'].items():
            if pos in k:
                status['nearest_link_pos'][pos] = v
        if pos not in status['nearest_link_pos']:
            nearest = get_nearest_link(pos, pos, remote_content)
            if nearest is not None:
                status['nearest_link_pos'][pos] = nearest

    return status

def get_nearest_link_with_bs(content, status, key):
    # TODO: Use python built-in function filter here (https://www.w3schools.com/python/ref_func_filter.asp)
    to_exclude = ['javascript:', 'facebook.','twitter.', 'google.',\
      'linkedin.', '#', 'mailto', 'viadeo.']
    bs = BeautifulSoup(content, 'lxml')
    for elem in bs.find_all(["a"]):
        # We assume not dirty at first, then we check
        dirty = False
        href = elem.attrs.get('href')
        txt = elem.text
        if href is not None and href != '' and href != '/' and trim_text(txt) is not None and trim_text(txt) != '':
            href = href.strip()
            txt = trim_text(txt)
            for _ in to_exclude:
                if _ in href:
                    dirty = True
                    break
            if not dirty:
                status[key][txt] = href
    return status

def get_full_all_links(status, base_url):
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
    return status

def get_full_nearest_links(status, base_url):
    keys = ['nearest_link_pos', 'nearest_link_neg']
    for _ in keys:
        for k, v in status[_].copy().items():
            if v:
                if v.startswith(base_url) is False:
                    if v.startswith('//'):
                        status[_][trim_text(k)] = 'http:' + v
                    elif v.startswith('http') is False:
                        status[_][trim_text(k)] = base_url + v
                if v.startswith('/'):
                    status[_][trim_text(k)] = base_url + v
    return status

def keyword_match(status, local_content, remote_content):#, detect_links=True):
    """ 
        Find diff pos, diff neg, nearest links pos, nearest links neg 
    """
    match_neg = list()
    match_pos = list()

    for keyword in status['keywords']:
        # print('\n\nKeyword === {}\n\n'.format(keyword))
        if not ' ' in keyword:
            for neg in status['diff_neg']:
                # print('sentence = {} / cleaned = {}'.format(neg, clean_sentence(neg)))
                if clean_sentence(neg) is None:
                    print('problem for --> {}'.format(neg))
                for word in clean_sentence(neg).split(' '):
                    # if keyword.lower() == 'ue':
                        # print('try to match <{}><{}> (RES:{})'.format(keyword.lower(), word, keyword.lower() == word))
                    if keyword.lower() == word and neg not in match_neg:
                        match_neg.append(neg)

            for pos in status['diff_pos']:
                if clean_sentence(pos) is None:
                    print('problem for --> {}'.format(pos))
                # print('sentence = {} / cleaned = {}'.format(pos, clean_sentence(pos)))
                for word in clean_sentence(pos).split(' '):
                    # if keyword.lower() == 'ue':
                        # print('try to match <{}><{}> (RES:{})'.format(keyword.lower(), word, keyword.lower() == word))
                    if keyword.lower() == word and pos not in match_pos:
                        match_pos.append(pos)
        else:
            for neg in status['diff_neg']:
                if clean_sentence(neg) is None:
                    print('problem for --> {}'.format(neg))
                # print('sentence = {} / cleaned = {}'.format(neg, clean_sentence(neg)))
                if keyword.lower() in clean_sentence(neg) and neg not in match_neg:
                    # if keyword.lower() == 'ue':
                        # print('try to match <{}><{}>'.format(keyword.lower(), neg))
                    match_neg.append(neg)

            for pos in status['diff_pos']:
                if clean_sentence(pos) is None:
                    print('problem for --> {}'.format(pos))
                # print('sentence = {} / cleaned = {}'.format(pos, clean_sentence(pos)))
                if keyword.lower() in clean_sentence(pos) and pos not in match_pos:
                    # if keyword.lower() == 'ue':
                        # print('try to match <{}><{}>'.format(keyword.lower(), neg))
                    match_pos.append(pos)
        
    status['diff_neg'] = match_neg
    status['diff_pos'] = match_pos
    return status

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]', 'b']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def extract_text_from_html(content):
    # Seems that if exception is kept inside this function, program does not stop
    try:
        if content is None:
            return content
        bs = BeautifulSoup(content, 'lxml') #lxml
        texts = bs.findAll(text=True)
        content = list(filter(tag_visible, texts))
    except Exception as e:
        print('Impossible to extract_text_from_html() : {}'.format(e))
        return None
    # Get rid of html or unicode space
    return [_.replace('\xa0', ' ') for _ in content]

def extract_links_from_html(content):
    links = list()
    webpage_regex = re.compile("""<a[^>]+href=["'](.*?)["']""", re.IGNORECASE)
    links = webpage_regex.findall(content)

    # TODO: Use python built-in function filter here (https://www.w3schools.com/python/ref_func_filter.asp)
    to_exclude = ['javascript:', 'facebook.','twitter.', 'google.',\
      'linkedin.', '#', 'mailto', 'viadeo.']

    excluded = set()
    for link in links:
        for word in to_exclude:
            if word in link:
                excluded.add(link)
    
    links = [_ for _ in links if (_ not in excluded and _ != '')]
    links = list(set(links))

    return links

def get_text_diff(local_content, remote_content, status, keywords_diff):#, detect_links=True):
    # extract content and links
    # print('REMOTE CONTENT : {}'.format(remote_content))
    try:
        extracted_local_content = extract_text_from_html(local_content)
        extracted_remote_content = extract_text_from_html(remote_content)
        # Save raw data for client 
        status['diff_raw_neg'] = [x for x in extracted_local_content if x not in extracted_remote_content]
        status['diff_raw_pos'] = [x for x in extracted_remote_content if x not in extracted_local_content]

        # get content diffs
        status['diff_neg'] = [x for x in extracted_local_content if x not in extracted_remote_content]
        status['diff_pos'] = [x for x in extracted_remote_content if x not in extracted_local_content]
            
        # taking off doublons in diff pos and diff neg    
        # Strip / Trim / Clean text
        status['diff_pos'] = [trim_text(x) for x in status['diff_pos'].copy() if trim_text(x) != ''] # was .strip() instead of trim_text
        status['diff_neg'] = [trim_text(x) for x in status['diff_neg'].copy() if trim_text(x) != ''] # was .strip() instead of trim_text
        
        # Set
        status['diff_pos'] = list(set(status['diff_pos'].copy()))
        status['diff_neg'] = list(set(status['diff_neg'].copy()))
        
        # Intersect
        intersect = set(status['diff_pos']).intersection(set(status['diff_neg']))
        status['diff_pos'] = [x for x in status['diff_pos'].copy() if x not in intersect]
        status['diff_neg'] = [x for x in status['diff_neg'].copy() if x not in intersect]

        if keywords_diff is True:
            # print('pass keyword match')
            status = keyword_match(status, local_content, remote_content)
        
        extracted_local_links = extract_links_from_html(local_content)
        extracted_remote_links = extract_links_from_html(remote_content)
        # if detect_links and status['diff_neg'] != []:
        if status['diff_neg'] != []:
            all_links_neg = set()
            [all_links_neg.add(x) for x in extracted_local_links if x not in extracted_remote_links]
            status['all_links_neg'].extend(all_links_neg)

        # if detect_links and status['diff_pos'] != []:
        if status['diff_pos'] != []:
            all_links_pos = set()
            [all_links_pos.add(x) for x in extracted_remote_links if x not in extracted_local_links]
            status['all_links_pos'].extend(all_links_pos)
        return status

    except Exception as e:
        print('get_text_diff exception -> {} (SoftTimeLimit() must have been raised)'.format(e))
        return None

def get_essential_content(content, min_sentence_len):
    extracted = extract_text_from_html(content)
    cleaned = clean_content(extracted, min_sentence_len)
    cleaned = list(map(str.strip, cleaned))
    cleaned = [x for x in cleaned if len(x.split(' ')) > min_sentence_len]
    cleaned = ' '.join(cleaned) # was ''
    cleaned = cleaned.replace('  ', ' ')
    if cleaned == '':
        return None
    else:
        return cleaned

def is_language(content, language):
    isReliable, textBytesFound, details = cld2.detect(content)
    if isReliable is True and details[0].language_name == language:
        return True
    return False

def is_valid_file(fname):
    # TODO: Use python built-in function filter here (https://www.w3schools.com/python/ref_func_filter.asp)
    to_include = ['.pdf', '.PDF']
    for _ in to_include:
        if _ in fname :
            return True
    if fname.startswith('.'):
        return False
    return False