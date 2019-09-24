import os
import http
import urllib
from urllib.request import urlopen
import ssl
import re
# import cld2
import pycld2 as cld2
import string
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

def clean_pdf_content(input_str):
    #print('-> cleaning pdf content ...')
    if input_str is None:
        return None
    intput_str = ''.join(x for x in input_str if x.isprintable())
    input_str = ''.join(input_str).lower()
    output = re.sub(r'[0-9]', '', input_str)
    t = str.maketrans('', '', string.punctuation)
    output = output.translate(t)
    output = ' '.join(output.split())
    return output

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
    
    # TODO: Add function to delete '-'s

    # get rid of cookie and javascript sentences
    to_exclude = ['cookie', 'javascript']
    for _ in to_exclude:
        output = [x for x in output if _ not in x]
    
    return output

def roundrobin(*iterables):
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
    preceding = elt.xpath('preceding::*/@href')[::-1]
    following = elt.xpath('following::*/@href')
    parent = elt.xpath('parent::*/@href')
    for href in roundrobin(parent, preceding, following):
        return href

def get_nearest_link(keyword, remote_content, url):
    nearest_link = []
    doc = LH.fromstring(remote_content)
    xpaths = doc.xpath('//*[contains(text(),{s!r})]'.format(s = keyword))
    len_xpaths = len(xpaths)
    #print('X Path = {}\n'.format(xpaths))
    for x in xpaths:
        nearest_link = [find_nearest(x)]
        #print('Nearsest link found (url) = {} ({})'.format(nearest_link, url))
        if len_xpaths > 1 and '#' not in nearest_link:
            print('Nearest founds are numerous for website : {}. Exit.'.format(url))
            break ;
    return nearest_link

def keyword_match(keywords, status, remote_content, url, detect_links=True):
    """ Find diff pos, diff neg, nearest links pos, nearest links neg """
    match_neg = list()
    match_pos = list()
    
    for keyword in keywords:
        for neg in status['diff_neg']:
            if keyword in neg:
                match_neg.append(neg)
                if detect_links:
                    status['nearest_link_neg'] = get_nearest_link(keyword, remote_content, url)
        for pos in status['diff_pos']:
            if keyword in pos:
                #print('**** <!> KEYWORD_MATCH : \'{}\' on url {} <!> ****'.format(keyword, status['url']))
                match_pos.append(pos)
                if detect_links:
                    status['nearest_link_pos'] = get_nearest_link(keyword, remote_content, url)

    status['diff_neg'] = match_neg
    status['diff_pos'] = match_pos

    if detect_links and status['diff_pos'] == []:
        status['all_links_pos'] = [] 
    if detect_links and status['diff_neg'] == []:
        status['all_links_neg'] = [] 
    return status

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def extract_text_from_html(content):
    bs = BeautifulSoup(content, 'lxml')
    texts = bs.findAll(text=True)
    content = list(filter(tag_visible, texts))
    return content

def extract_links_from_html(content):
    links = list()
    webpage_regex = re.compile("""<a[^>]+href=["'](.*?)["']""", re.IGNORECASE)
    links = webpage_regex.findall(content)
    return links



def get_text_diff(local_content, remote_content, status, detect_links=True):
    # extract content and links
    extracted_local_content = extract_text_from_html(local_content)
    extracted_remote_content = extract_text_from_html(remote_content)
    if detect_links:
        extracted_local_links = extract_links_from_html(local_content)
        extracted_remote_links = extract_links_from_html(remote_content)
    # clean content ('\n' here)
    extracted_local_content = clean_content(extracted_local_content)
    extracted_remote_content = clean_content(extracted_remote_content)
    # get content diffs
    status['diff_neg'] = [x for x in extracted_local_content if x not in extracted_remote_content]
    status['diff_pos'] = [x for x in extracted_remote_content if x not in extracted_local_content]

    if detect_links and status['diff_neg'] != []:
        all_links_neg = set()
        [all_links_neg.add(x) for x in extracted_local_links if x not in extracted_remote_links]
        status['all_links_neg'] = list(all_links_neg)
        #print('diff all links neg = {}'.format(status['all_links_neg']))
    else:
        status['all_links_neg'] = None

    if detect_links and status['diff_pos'] != []:
        all_links_pos = set()
        [all_links_pos.add(x) for x in extracted_remote_links if x not in extracted_local_links]
        status['all_links_pos'] = list(all_links_pos)
        #print('diff all links pos = {}'.format(status['all_links_pos']))
    else:
        status['all_links_pos'] = None
        
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
'''
def extract_html(full_url, link):
    print('HTML -> {}'.format(link))
    html = scrapper.get_url_content(full_url + link)
    if html is None:
        return None
    html = html.encode('utf-8')
    bs = BeautifulSoup(html, 'html.parser')
    texts = bs.findAll(text=True)
    extracts = filter(tag_visible, texts)
    return list(extracts)
'''