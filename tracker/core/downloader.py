import os
import re
import lxml
from bs4 import BeautifulSoup
import urllib
import urllib.request
import requests
from socket import timeout
import ssl
import time
import random
import tracker.core.crawler as crawler
import tracker.core.scrapper as scrapper
import tracker.core.logger as logger
import tracker.core.utils as utils
import tracker.core.extractor as extractor
import http.client

def allow_create_folder(current_path):
    if os.path.isfile(current_path):
        try:
            os.rename(current_path, current_path + '___')
            print('[REC]: Filename {} changed into {}'.format(current_path, current_path + '___'))
            return
        except Exception as e:
            print('[RECURSION]: Not possible to rename {} into {}, file already exists !'.format(current_path, current_path + '___'))
            return
    else:
        allow_create_folder(current_path.rpartition('/')[0])

def download_and_save_content(url, name, path, header, check_duplicates=False, replace=False):
    """ For each website link, download the content found on link.
        Checks whether there are no duplicates. If name of file is '',
        name becomes 'unknown___'. If name of file matches an already
        existing directory name, name becomes: 'directoryname' + '___' 
        at the end to differentiate and keep directories architecture.
        args:
            url (str): Complete url to be crawled
            name (str): Name of the file to save url
            path (str): Full path of where to put the file
            header (dict): Header to use for the request
        kwarg:
            check_duplicates (bool): Make sure no duplicate in names (default:False)
    """
    #print('FULL URL ARRIVED -------> {}'.format(url))
    if not os.path.isdir(path):
        # if there is a file with same name as folder, change its name
        if check_duplicates:
            if os.path.isfile(path):
                os.rename(path, path + '___')
                print('path: {} is not a directory, changing name to unknown___'.format(path))
        try:
            os.makedirs(path)
        except Exception as e:
            print('Not possible to create directory {}, coming up in depth to fix it..'.format(path))
            allow_create_folder(path)
            os.makedirs(path)
        # and now can create directory
        
    if check_duplicates and name == '':
        name = 'unknown___'
    full_path = os.path.join(path, name)
    if check_duplicates and os.path.isdir(full_path):
        full_path = full_path + '___'
    if replace is False and os.path.isfile(full_path):
        print('\'{}\' already exists.\n'.format(full_path))
        return
    elif replace is True and os.path.isfile(full_path):
        print('Replace option activated, removing file : {}'.format(full_path))
        os.remove(full_path)
        print('Successfuly REMOVED.')
        
    req = urllib.request.Request(
            url,
            data=None,
            headers=header
    )
    # Faking SSL certificate to avoid unauthorized requests
    gcontext = ssl._create_unverified_context()
    try:
        # download content of the url
        response = urllib.request.urlopen(req, context=gcontext, timeout=30)
    except (urllib.error.HTTPError, urllib.error.URLError, ConnectionResetError, UnicodeDecodeError) as e:
        print('[ERROR] download_and_save_content : {}\n(url = {})'.format(e, url))
        return None
    except timeout:
        print('[ERROR TIMEOUT] for url : {}'.format(url))
        return None
    # Save content in the provided path with binary format
    with open (full_path, 'wb+') as content:
        try:
            content.write(response.read())
        except (http.client.IncompleteRead) as e:
            print('[ERROR] - Incomplete Read. Skipping download for this file. Details = {}'.format(e))
            return None

def download_website(links, base_path, url, random_header=False):
    """ Loop through all links and download the content if not already downloaded
        args:
            links (list): List of links to download (URIs)
            base_path (str): Path where to store content (default: '/data_path/www.*.com/website_content')
            url (str): Base url to append URIs to
        kwarg:
            random_header (bool): If True, use a different header for each request (default: False)
    """
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
    counter = 0
    total = len(links)
    for link in links:
        counter += 1
        if random_header:
            header = utils.rh()
        filename = link.rpartition('/')[2]
        print('Filename : {}\n\n'.format(filename))
        ''''
        print('#LINK = {}'.format(link))
        if link.startswith('<PDF> http'):
            dir_path = os.path.join(base_path, '__external_files__' )
            full_url = link.replace('<PDF> ', '')
        elif link.startswith('<EXCEL> http'):
            dir_path = os.path.join(base_path, '__external_files__' )
            full_url = link.replace('<EXCEL> ', '')
        else:
        '''
        dir_path = os.path.join(base_path, utils.find_internal_link(link).rpartition('/')[0][1:])
        print('Saving file in {}'.format(dir_path))
        full_url = url + utils.find_internal_link(link)
        print('URL + LINK : {}'.format(full_url))
        assert dir_path.startswith(base_path)
        if link.startswith('/'):
            download_and_save_content(full_url, filename, dir_path, header, check_duplicates=True)
        '''
        elif link.startswith('<PDF>') or link.startswith('<EXCEL>'):
            download_and_save_content(full_url, filename, dir_path, header)
            print('EXCEL -> {}'.format(link))
        elif link.startswith('<ERROR>'):
            print('ERROR -> {}'.format(link))
        '''
    return True

def download_website_diff(links, base_path, diff_path, url):
    """ Try to download website parts that have changed """
    random.shuffle(links)
    for link in links:
        time.sleep(random.randint(0, 10))
        base_dir_path = os.path.join(base_path, utils.find_internal_link(link).rpartition('/')[0][1:])
        filename = link.rpartition('/')[2]
        full_url = url + utils.find_internal_link(link)
        base_dir_path_file = os.path.join(base_dir_path, filename)
        if os.path.isdir(base_dir_path_file) and os.path.isfile(base_dir_path_file + '___'):
            base_dir_path_file = base_dir_path_file + '___'

        # getting local file content
        print('\n-> Opening base_dir_path_file = {}'.format(base_dir_path_file))

        local_content = scrapper.get_local_content(base_dir_path_file, 'rb')
        
        # getting full_url content
        print('-> Getting content of webpage to compare : {}'.format(full_url))
        
        remote_content = scrapper.get_url_content(full_url, header=utils.rh())

        extracted_local_content = extractor.extract_text_from_html(local_content)
        extracted_local_content = extractor.clean_content(extracted_local_content)
        extracted_remote_content = extractor.extract_text_from_html(remote_content)
        extracted_remote_content = extractor.clean_content(extracted_remote_content)

        #print('REMOTE CONTENT = {}\n'.format(remote_content))

        extracted_diff_minus = [x for x in extracted_local_content if x not in extracted_remote_content]
        extracted_diff_plus = [x for x in extracted_remote_content if x not in extracted_local_content]

        print('\n\n DIFF +++ :\n{}'.format(extracted_diff_plus))
        print('\n\n DIFF --- :\n{}'.format(extracted_diff_minus))
        #exit(0)
        if len(extracted_diff_plus) > 1 or len(extracted_diff_minus) > 1:
            print('***** Content is different *****')
        else:
            print('***** Content is SIMILAR *****')
        
