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
        intput_str = ''.join(x for x in input_str if x.isprintable())
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
    # preceding = elt.xpath('preceding::*/@href')[::-1]
    # following = elt.xpath('following::*/@href')
    # parent = elt.xpath('parent::*/@href')
    # print('preceding : \n{}\n\nfollowing : {}\n\nparent : {}\n\n'.format(preceding, following, parent))
    # for href in roundrobin(parent, preceding, following):
    #     return href

def get_nearest_link(match, keyword, content):

    nearest_link = dict()
    # print('looking for kw ========> {}'.format(match))
    # match = match.replace('\xa0', ' ')
    doc = LH.fromstring(content.replace('\'', ' '))
    print('ASKED TO FIND FOLLOWINF MATCH ->{}<-'.format(match))
    el2 = doc.xpath('//a[text()={s!r}]/@href'.format(s = match))
    # el2 = doc.xpath('/html/body//a[contains(text(),{s!r})]/@href'.format(s = match))
    if el2 != []:
        print('HERE el2 not None -> {}'.format(el2))
        print('el2 = {}'.format(el2))
        if '#' not in el2[0] and (el2[0].startswith('/') or el2[0].startswith('http')):
            nearest_link.update({match: el2[0]})
        return nearest_link
    else:
    #     return []
    
        print('* el2 is None *')
        for x in doc.xpath('//*[contains(text(),{s!r})]'.format(s = match)):
            nearest = find_nearest(x)
            print('nearest => {}'.format(nearest))
            # if not nearest.startswith('http'):
                # nearest_link.update({match: url + nearest})
            # else:
            if '#' not in nearest and (nearest.startswith('/') or nearest.startswith('http')):
                nearest_link.update({match:nearest})

        # print('el2 is None rr')

        return nearest_link

def nearest_link_match(status, local_content, remote_content, url):

    """ Find diff pos, diff neg, nearest links pos, nearest links neg """
    # remote_content = remote_content.decode('utf8').replace('<b>', '').replace('</b>', '')
    #print('REMOTEEE FROM HERE : {}'.format(remote_content))
    for neg in status['diff_neg']:
        status['nearest_link_neg'].update(get_nearest_link(neg, neg, local_content))

    for pos in status['diff_pos']:
        status['nearest_link_pos'].update(get_nearest_link(pos, pos, remote_content))

    return status

def nearest_link_match_bs(status, local_content, remote_content, url):

    for neg, pos in zip(status['diff_neg'], status['diff_pos']):
        for nl, nr in zip(list(status['all_nearest_links_local'].keys()), list(status['all_nearest_links_remote'].keys())):
            if neg in nl:
                status['nearest_link_neg'][neg] = status['all_nearest_links_local'][nl]
            if pos in nr:
                status['nearest_link_pos'][pos] = status['all_nearest_links_remote'][nr]

    # for neg in status['diff_neg']:
    #     for k, v in status['all_nearest_links_local'].items():
    #         # print('k = {}, v = {}'.format(k, v))
    #         if neg in k:
    #             status['nearest_link_neg'][neg] = v

    # for pos in status['diff_pos']:
    #     for k, v in status['all_nearest_links_remote'].items():
    #         # print('k = {}, v = {}'.format(k, v))
    #         if pos in k:
    #             status['nearest_link_pos'][pos] = v

    return status

def get_nearest_link_with_bs(content, status, key):
    bs = BeautifulSoup(content, 'lxml')
    for elem in bs.find_all(["a"]):
        href = elem.attrs.get('href')
        txt = elem.text
        status[key][txt] = href
    return status

def keyword_match(keywords, status, local_content, remote_content, url, detect_links=True):
    """ Find diff pos, diff neg, nearest links pos, nearest links neg """
    # remote_content = remote_content.decode('utf8').replace('<b>', '').replace('</b>', '')
    #print('REMOTEEE FROM HERE : {}'.format(remote_content))

    match_neg = list()
    match_pos = list()

    # print('KEYWORRRRRDS ::: {}'.format(keywords))
    #print('DIFF NEGATIVE = {}'.format(status['diff_neg']))
    # print('DIFF POSITIVE = {}'.format(status['diff_pos']))

    if isinstance(keywords, list) and len(keywords) == 1:
        keywords = keywords[0].split(';')
    for keyword in keywords:

        # print('\n\nKeyword === {}\n\n'.format(keyword))
        if not ' ' in keyword:
            for x in status['diff_neg']:
                neg = x#.replace('\xa0', ' ')
                # print('sentence = {} / cleaned = {}'.format(neg, clean_sentence(neg)))
                for word in clean_sentence(neg).split(' '):
                    if 'sqli' in word.lower():
                        print('try to match <{}><{}>'.format(keyword.lower(), word.lower()))
                    if keyword.lower() == word and neg not in match_neg:
                        match_neg.append(neg)
                        if detect_links:
                            for k, v in status['all_nearest_links_local'].items():
                                if neg in k:
                                    status['nearest_link_neg'][neg] = v
                                    # break

            for x in status['diff_pos']:
                pos = x#.replace('\xa0', ' ')
                # print('sentence = {} / cleaned = {}'.format(pos, clean_sentence(pos)))
                for word in clean_sentence(pos).split(' '):
                    # print('try to match <{}><{}>'.format(keyword.lower(), word))
                    if keyword.lower() == word and pos not in match_pos:
                        match_pos.append(pos)
                        if detect_links:
                            for k, v in status['all_nearest_links_remote'].items():
                                if pos in k:
                                    status['nearest_link_pos'][pos] = v
                                    # break
        
        else:
            for x in status['diff_neg']:
                neg = x#.replace('\xa0', ' ')
                if keyword.lower() in clean_sentence(neg) and neg not in match_neg:
                    if 'sqli' in keyword.lower():
                        print('try to match <{}><{}>'.format(keyword.lower(), neg))
                    match_neg.append(neg)
                    if detect_links:
                        for k, v in status['all_nearest_links_local'].items():
                            if neg in k:
                                status['nearest_link_neg'][neg] = v
                                # break

            for x in status['diff_pos']:
                pos = x#.replace('\xa0', ' ')
                if keyword.lower() in clean_sentence(pos) and pos not in match_pos:
                    match_pos.append(pos)
                    if detect_links:
                        for k, v in status['all_nearest_links_remote'].items():
                            if pos in k:
                                status['nearest_link_pos'][pos] = v
                                # break
        
    status['diff_neg'] = match_neg#[_.replace('\xa0', ' ') for _ in match_neg]
    status['diff_pos'] = match_pos#[_.replace('\xa0', ' ') for _ in match_pos]
    print('diff neg == {}'.format(status['diff_neg']))
    print('diff pos == {}'.format(status['diff_pos']))

    # TODO: Maybe let all links diff anyway ? In this case, need to change condition (of 
    # showing diff pos or diff neg) in tracker.mail
    if detect_links and status['diff_pos'] == []:
        status['all_links_pos'] = [] 
    if detect_links and status['diff_neg'] == []:
        status['all_links_neg'] = []
    # print('url : {}\n->all links pos = {}\n->all links neg = {}\n'.format(url, status['all_links_pos'], status['all_links_neg']))
    
    return status

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]', 'b']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def extract_text_from_html(content):
    if content is None:
        return content
    bs = BeautifulSoup(content, 'lxml') #lxml
    texts = bs.findAll(text=True)
    content = list(filter(tag_visible, texts))

    # Get rid of html or unicode space
    return [_.replace('\xa0', ' ') for _ in content]
    #[_.encode('ascii', errors='ignore').decode('ascii', errors='ignore') for _ in content]

def extract_links_from_html(content):
    links = list()
    # if isinstance(content, bytes):
        # content = content.decode('utf-8', errors='ignore')
    webpage_regex = re.compile("""<a[^>]+href=["'](.*?)["']""", re.IGNORECASE)
    links = webpage_regex.findall(content)

    to_exclude = ['javascript:', 'facebook.','twitter.',\
     'youtube.', 'instagram.', 'google.',\
      'linkedin.', '#', 'mailto', 'viadeo.']
    excluded = set()
    for link in links:
        for word in to_exclude:
            if word in link:
                excluded.add(link)
    
    links = [_ for _ in links if _ not in excluded]
    links = list(set(links))

    return links



def get_text_diff(local_content, remote_content, status, detect_links=True):
    # extract content and links
    # print('REMOTE CONTENT : {}'.format(remote_content))
    extracted_local_content = extract_text_from_html(local_content)
    extracted_remote_content = extract_text_from_html(remote_content)
    if detect_links:
        extracted_local_links = extract_links_from_html(local_content)
        extracted_remote_links = extract_links_from_html(remote_content)
    # clean content ('\n' here)
    # Save raw data for client 
    status['diff_raw_neg'] = [x for x in extracted_local_content if x not in extracted_remote_content]
    status['diff_raw_pos'] = [x for x in extracted_remote_content if x not in extracted_local_content]

    # get content diffs
    status['diff_neg'] = [x for x in extracted_local_content if x not in extracted_remote_content]
    status['diff_pos'] = [x for x in extracted_remote_content if x not in extracted_local_content]

    if detect_links and status['diff_neg'] != []:
        all_links_neg = set()
        [all_links_neg.add(x) for x in extracted_local_links if x not in extracted_remote_links]
        status['all_links_neg'].extend(all_links_neg)

    if detect_links and status['diff_pos'] != []:
        all_links_pos = set()
        [all_links_pos.add(x) for x in extracted_remote_links if x not in extracted_local_links]
        status['all_links_pos'].extend(all_links_pos)
        
    # taking off doublons in diff pos and diff neg    
    # Strip
    status['diff_pos'] = [x.strip() for x in status['diff_pos'].copy()]
    status['diff_neg'] = [x.strip() for x in status['diff_neg'].copy()]
    
    # Set
    status['diff_pos'] = list(set(status['diff_pos'].copy()))
    status['diff_neg'] = list(set(status['diff_neg'].copy()))
    
    # Intersect
    intersect = set(status['diff_pos']).intersection(set(status['diff_neg']))
    status['diff_pos'] = [x for x in status['diff_pos'].copy() if x not in intersect]
    status['diff_neg'] = [x for x in status['diff_neg'].copy() if x not in intersect]
        
    return status

def get_essential_content(content, min_sentence_len):
    extracted = extract_text_from_html(content)
    cleaned = clean_content(extracted, min_sentence_len)
    cleaned = list(map(str.strip, cleaned))
    cleaned = [x for x in cleaned if len(x.split(' ')) > min_sentence_len]
    cleaned = ''.join(cleaned)
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
    to_include = ['.pdf', '.PDF']
    for _ in to_include:
        if _ in fname :
            return True
    if fname.startswith('.'):
        return False
    return False