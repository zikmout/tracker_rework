import os
import http
import urllib
from urllib.request import urlopen
import ssl
import re
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
    for x in xpaths:
        nearest_link = [find_nearest(x)]
        print('Nearsest link found = {}'.format(nearest_link))
        if len_xpaths > 1:
            print('Nearest founds are numerous for website : {}. Exit.'.format(url))
            break ;
    return nearest_link

def keyword_match(keywords, status, remote_content, url):
    match_neg = list()
    match_pos = list()
    
    for keyword in keywords:
        for neg in status['diff_neg']:
            if keyword in neg:
                match_neg.append(neg)
                status['nearest_link_neg'] = get_nearest_link(keyword, remote_content, url)
        for pos in status['diff_pos']:
            if keyword in pos:
                print('**** <!> KEYWORD_MATCH : \'{}\' on url {} <!> ****'.format(keyword, status['url']))
                match_pos.append(pos)
                status['nearest_link_pos'] = get_nearest_link(keyword, remote_content, url)

    status['diff_neg'] = match_neg
    status['diff_pos'] = match_pos

    if status['diff_pos'] == []:
        status['all_links_pos'] = [] 
    if status['diff_neg'] == []:
        status['all_links_neg'] = [] 
    return status

def clean_content(input_list):
    """ Method that clean every element of a list
        arg:
            input_list(list): List of elements to be cleaned
        return:
            ouput (list): List of cleaned elements
    """
    output = [x for x in input_list if x != '\n']
    #t = str.maketrans("\n\t\r", "   ")
    #output = [x.translate(t) for x in output]
    #output = [x.strip() for x in output]
    return output

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



def get_text_diff(local_content, remote_content, status):
    # extract content and links
    extracted_local_content = extract_text_from_html(local_content)
    extracted_local_links = extract_links_from_html(local_content)
    extracted_remote_content = extract_text_from_html(remote_content)
    extracted_remote_links = extract_links_from_html(remote_content)
    # clean content ('\n' here)
    extracted_local_content = clean_content(extracted_local_content)
    extracted_remote_content = clean_content(extracted_remote_content)
    # get content diffs
    status['diff_neg'] = [x for x in extracted_local_content if x not in extracted_remote_content]
    status['diff_pos'] = [x for x in extracted_remote_content if x not in extracted_local_content]
    if status['diff_neg'] != []:
        all_links_neg = set()
        [all_links_neg.add(x) for x in extracted_local_links if x not in extracted_remote_links]
        status['all_links_neg'] = list(all_links_neg)
        print('diff all links neg = {}'.format(status['all_links_neg']))
    if status['diff_pos'] != []:
        all_links_pos = set()
        [all_links_pos.add(x) for x in extracted_remote_links if x not in extracted_local_links]
        status['all_links_pos'] = list(all_links_pos)
        print('diff all links pos = {}'.format(status['all_links_pos']))
    return status



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