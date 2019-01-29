import os
from urllib.request import urlopen
import ssl
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
import pintell.core.scrapper as scrapper

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

def get_nearest_link(remote_content, keyword, url, full_url):
    nearest_link = []
    doc = LH.fromstring(remote_content)
    xpaths = doc.xpath('//*[contains(text(),{s!r})]'.format(s = keyword))
    len_xpaths = len(xpaths)
    for x in xpaths:
        nearest_link = find_nearest(x)
        if nearest_link.startswith(url) is False:
            nearest_link = url + nearest_link
        print('Nearsest link found = {}'.format(nearest_link))
        if len_xpaths > 1:
            print('Nearest founds are numerous for website : {}. Exit.'.format(full_url))
            break ;
    return nearest_link

def keyword_match(keywords, diff_neg, diff_pos, remote_content, full_url, url):
    match_neg = list()
    match_pos = list()
    nearest_link_pos = list()
    nearest_link_neg = list()
    for keyword in keywords:
        for neg in diff_neg:
            if keyword in neg:
                match_neg.append(neg)
                nearest_link_neg = get_nearest_link(remote_content, keyword, url, full_url)
        for pos in diff_pos:
            if keyword in pos:
                print('**** <!> KEYWORD_MATCH : \'{}\' on url {} <!> ****'.format(keyword, full_url))
                match_pos.append(pos)
                nearest_link_pos = get_nearest_link(remote_content, keyword, url, full_url)
                
    return match_neg, match_pos, nearest_link_pos, nearest_link_neg

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

def get_text_diff(local_content, remote_content):
    # extract content
    extracted_local_content = extract_text_from_html(local_content)
    extracted_remote_content = extract_text_from_html(remote_content)
    # clean content ('\n' here)
    extracted_local_content = clean_content(extracted_local_content)
    extracted_remote_content = clean_content(extracted_remote_content)
    # get all diffs
    diff_neg = [x for x in extracted_local_content if x not in extracted_remote_content]
    diff_pos = [x for x in extracted_remote_content if x not in extracted_local_content]
    return diff_pos, diff_neg

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

def read_pdf(pdf_file):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)

    PDFPage.get_pages(rsrcmgr, device, pdf_file)
    device.close()

    content = retstr.getvalue()
    retstr.close()
    return content

def extract_pdf(full_url, link):
    print('FULL URL => {}'.format(full_url + link))
    pdf = urlopen(full_url + link)
    #pdf = get_response_from_url(full_url + link)
    #print('PDF ->>>> {}'.format(type(pdf)))
    output_string = read_pdf(pdf)
    print(output_string)
    pdf.close()
'''
