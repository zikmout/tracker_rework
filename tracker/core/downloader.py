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

from pprint import pprint

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# from pyvirtualdisplay import Display

class AdidasScraper:
    """ for website https://www.adidas-group.com/en/investors/investor-events/ only
    """
    def __init__(self, url):
        # self.display = Display(visible=0, size=(800, 600))
        # self.display.start()
        self.url = url
        # binary = FirefoxBinary('/Users/xxx/')
        # self.driver = webdriver.Firefox(firefox_binary=binary)
        #options = FirefoxOptions()
        #options.add_argument("--headless")
        options = FirefoxOptions()
        options.headless = True
        self.driver = webdriver.Firefox(options=options)

    def get_html_wait(self):#, max_company_count=1000):
        """Extracts and returns company links (maximum number of company links for return is provided)."""
        self.driver.implicitly_wait(15)
        self.driver.get(self.url)
        # elements = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/article/section/div/section[2]')))
        # text = elements.html
        html = self.driver.page_source
        #print('\n\npage source --------> \n\n{}\n\n'.format(html))
        # elements = self.driver.find_element_by_class_name("events future visible")
        # element = WebDriverWait(self.driver, 15).until(
        #     EC.presence_of_element_located((By.CLASS_NAME, "events future visible"))
        # )
        self.driver.quit()
        # self.driver.close()
        # self.display.stop()
        return html

def allow_create_folder(current_path):
    if os.path.isfile(current_path) and not os.exists(current_path + '___'):
        try:
            os.rename(current_path, current_path + '___')
            print('[REC]: Filename {} changed into {}'.format(current_path, current_path + '___'))
            return
        except Exception as e:
            print('[RECURSION]: Not possible to rename {} into {}, file already exists !'.format(current_path, current_path + '___'))
            return
    else:
        allow_create_folder(current_path.rpartition('/')[0])

def save_remote_content(remote_content, url, path, name, check_duplicates=False):
    print('< Asked to save remote_content on disk > url: {} (utils find internal link = {}'.format(url, utils.find_internal_link(path)))
    if url.endswith('/') or name == '':
        name = 'unknown___'
    if not os.path.isdir(path):
        print('** PATH =>>>> {}'.format(path))
        # if there is a file with same name as folder, change its name
        if check_duplicates:
            if os.path.isfile(path):
                os.rename(path, path + '___')
                print('** path: {} is not a directory, changing name to unknown___'.format(path))
        try:
            os.makedirs(path)
        except Exception as e:
            print('Not possible to create directory {}, coming up in depth to fix it..'.format(path))
            allow_create_folder(path)
            os.makedirs(path)
        except Exception as e:
            print('[ERROR] - save_remote_content : {}'.format(e))
            return False

    # Save content in the provided path with binary format
    full_path = os.path.join(path, name)
    with open (full_path, 'wb+') as content:
        try:
            #print('TT REMOTE COTENT = {}'.format(type(remote_content)))
            if not isinstance(remote_content, bytes):
                content.write(remote_content.encode('utf-8'))
            else:
                content.write(remote_content)
            #content.write(response.read())
        except (http.client.IncompleteRead) as e:
            print('[ERROR] - save_remote_content : {}'.format(e))
            return False
    return True
 
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
    print('FULL URL ARRIVED -------> {}'.format(url))
    if url.endswith('/'):
        name = 'unknown___'
        print('Changing name to unknown')
    else:
        print('NO NEED TO CHANGE NAME TO UNKNOWN')
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
    checked=False
    try:
        # download content of the url
        response = urllib.request.urlopen(req, context=gcontext, timeout=12)
        # remote_content = response.read()#.decode('utf-8', errors='ignore')
        # response.close()
    except (urllib.error.HTTPError, urllib.error.URLError, ConnectionResetError, UnicodeDecodeError) as e:
        print('[ERROR] download_and_save_content : {}\n(url = {})'.format(e, url))
        return { url : '[URL ERROR] {}'.format(e)}
    except (urllib.error.URLError, timeout, TimeoutError) as e:
        print('[ERROR TIMEOUT] for url : {} (Error : {})'.format(url, e))
        print('\n-------------> TIMEOUT ERROR CATCHED <----------------\n')
        print('Retrying HTTP request now ...\n')
        scraper = AdidasScraper(url)
        remote_content = scraper.get_html_wait()
        # print('Return from scrapper2 =======>> {}'.format(remote_content))
        msg = '{}'.format(e)
        error = { url: msg }
        checked = True
    # except Exception as e:
    #     remote_content = None
    #     msg = '{}'.format(e)
    #     error = { url: msg }
    #     print('ERROR : url = {}, message => {}'.format(url, msg))
    # return remote_content, error
        # return { url : '[TIMEOUT--]'}
    # Save content in the provided path with binary format
    with open (full_path, 'wb+') as content:
        try:
            if checked:
                content.write(remote_content.encode('utf-8'))
            else:
                content.write(response.read())
                response.close()
        except (http.client.IncompleteRead) as e:
            print('[ERROR] - Incomplete Read. Skipping download for this file. Details = {}'.format(e))
            response.close()
            return { url : '[INCOMPLETE READ] {}'.format(e) }
    return { url : 'TargetURL was not found on local storage. Successfuly downloaded.'}

def download_website(links, base_path, url, random_header=False):
    """ Loop through all links and download the content if not already downloaded
        args:
            links (list): List of links to download (URIs)
            base_path (str): Path where to store content (default: '/data_path/www.*.com/website_content')
            url (str): Base url to append URIs to
        kwarg:
            random_header (bool): If True, use a different header for each request (default: False)
    """
    rets = list() # rets is like : [{ url : '[TIMEOUT]'}, ...]
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
            rets.append(download_and_save_content(full_url, filename, dir_path, header, check_duplicates=True))
        '''
        elif link.startswith('<PDF>') or link.startswith('<EXCEL>'):
            download_and_save_content(full_url, filename, dir_path, header)
            print('EXCEL -> {}'.format(link))
        elif link.startswith('<ERROR>'):
            print('ERROR -> {}'.format(link))
        '''
    return rets

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
        
        remote_content, error_remote_content = scrapper.get_url_content(full_url, header=utils.rh())

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
        
def make_request_for_updating_content(user_email, project_name, urls):
    # Making synchronous HTTP Request (because workers are aynchronous already)
    post_data = { 'user_email': user_email, 'project_name': project_name, 'urls': urls }
    body = json.dumps(post_data)

    http_client = httpclient.HTTPClient()
    try:
        response = http_client.fetch('http://localhost:5567/api/v1/update-content', method='POST', body=body)
        http_client.close()
        return response.body
    except Exception as e:
        error_str = 'Error making request for updating content ({})'.format(e)
        print('Error -> {}'.format(error_str))
        http_client.close()
        return json.dumps({ 'error': '{}'.format(error_str)})