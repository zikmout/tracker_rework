import os
import re
import lxml
from bs4 import BeautifulSoup
import urllib
import urllib.request
import requests
import ssl
import crawler
import scrapper
import logger
import utils
import extractor
from lxml.html.diff import htmldiff

def download_page():
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.142 Safari/535.19'}
    url = 'https://www.airfranceklm.com'
    req = urllib.request.Request(
            url,
            data=None,
            headers=header
    )
    # Faking SSL certificate to avoid unauthorized requests
    gcontext = ssl._create_unverified_context()
    try:
        response = urllib.request.urlopen(req, context=gcontext)
    except (urllib.error.HTTPError, urllib.error.URLError, ConnectionResetError, UnicodeDecodeError) as e:
        print('[ERROR] download_and_save_content : {}'.format(e))
        return None        
    
    with open ('/Users/xxx/Projects/SBB/afklm', 'wb+') as content:
        content.write(response.read())

def clean_content(input_list):
    output = [x for x in input_list if x != '\n']
    t = str.maketrans("\n\t\r", "   ")
    output = [x.translate(t) for x in output]
    output = [x.strip() for x in output]
    return output

def compare_pages():
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.142 Safari/535.19'}
    url = 'https://www.airfranceklm.com'
    req = urllib.request.Request(
            url,
            data=None,
            headers=header
    )
    # Faking SSL certificate to avoid unauthorized requests
    gcontext = ssl._create_unverified_context()
    try:
        response = urllib.request.urlopen(req, context=gcontext)
    except (urllib.error.HTTPError, urllib.error.URLError, ConnectionResetError, UnicodeDecodeError) as e:
        print('[ERROR] download_and_save_content : {}'.format(e))
        return None   

    remote_content = response.read().decode('utf-8')

    fd_local = open('/Users/xxx/Projects/SBB/afklm', 'rb')
    local_content = fd_local.read().decode('utf-8')
    fd_local.close()
        
    bs = BeautifulSoup(local_content, 'html.parser')
    texts = bs.findAll(text=True)
    local_content = list(filter(extractor.tag_visible, texts))
    '''    
    for x in local_content:
        ' '.join([line.strip() for line in x.strip().splitlines()])
        #local_content = ''.join(local_content)
    '''
    bs = BeautifulSoup(remote_content, 'html.parser')
    texts = bs.findAll(text=True)
    remote_content = list(filter(extractor.tag_visible, texts))

    remote_content = clean_content(remote_content)
    local_content = clean_content(local_content)

    diff = list()
    diff1 = [x for x in local_content if x not in remote_content]
    diff2 = [x for x in remote_content if x not in local_content]        

    print('\n\n DIFF UN SENS:\n{}'.format(diff1))
    print('\n\n DIFF DEUX SENS:\n{}'.format(diff2))
    print('DIFFFFFF:\n')
    print(diff)

download_page()
#compare_pages()
