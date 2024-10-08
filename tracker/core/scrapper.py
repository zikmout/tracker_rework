import os
import urllib
import urllib.request
import ssl
from ssl import SSLError
import time
import requests
from socket import timeout

# Taken from : https://codereview.stackexchange.com/questions/167327/scraping-the-full-content-from-a-lazy-loading-webpage
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tracker.core.utils as utils
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from pyvirtualdisplay import Display

class AdidasScraper2:
    """ for website https://www.adidas-group.com/en/investors/investor-events/ only
    """
    def __init__(self, url):
        self.url = url
        self.options = FirefoxOptions()
        self.options.headless = True

    def get_html_wait(self):
        """Extracts and returns company links (maximum number of company links for return is provided)."""
        try:
            driver = webdriver.Firefox(options=self.options)
            driver.implicitly_wait(15)
            driver.get(self.url)
            html = driver.page_source
            # print('Here is the page source = {}'.format(html))
        finally:
            driver.quit()
        return html

class AdidasScraper:
    """ for website https://www.adidas-group.com/en/investors/investor-events/ only
    """
    def __init__(self, url):
        self.url = url
        
    def get_html_wait(self):#, max_company_count=1000):
        """Extracts and returns company links (maximum number of company links for return is provided)."""
        display = Display(visible=0, size=(800, 600))
        display.start()
        try:
            browser = webdriver.Firefox()
            browser.implicitly_wait(15)
            browser.get(self.url)
            html = browser.page_source
        finally:
            browser.quit()
            display.stop()
        return html

def get_url_content(url, header, verbose=True):
    """ Open remote website content
        args:
            url (str): Full url of remote content to access
            header (dict): Header to use when accessing content
        return:
            remote_content: Binary content decoded
    """
    error = None
    # Faking User-Agent to avoid forbidden requests
    req = urllib.request.Request(url, data=None, headers=utils.rh())
    # Faking SSL certificate to avoid unauthorized requests
    gcontext = ssl._create_unverified_context()

    try:
        # download content of the url
        response = urllib.request.urlopen(req, context=gcontext, timeout=12)
        remote_content = response.read()#.decode('utf-8', errors='ignore')
        response.close()
    except (timeout, TimeoutError, SSLError) as e:
        print('[ERROR TIMEOUT OR SSL] for url : {} (Error : {})'.format(url, e))
        print('Retrying HTTP request now ...\n')
        scraper = AdidasScraper2(url)
        remote_content = scraper.get_html_wait()
        return remote_content, {url : '{}'.format(e)}
    except (urllib.error.URLError, urllib.error.HTTPError, ConnectionResetError, UnicodeDecodeError) as e:
        print('[ERROR] {} : {}\n'.format(url, e))
        return None, {url : '{}'.format(e)}

    return remote_content, {url : ''}


def get_local_content(path, mode):
    """ Open local file content
        args:
            path (str): Full path of file to open
            mode (str): Mode of file opening (e.g. 'rb')
        return:
            local_content: Binary content decoded
    """
    try:
        fd = open(path, mode)
        local_content = fd.read().decode('utf-8', errors='ignore')
        fd.close()
        return local_content
    except Exception as e:
        print('Problem reading local content : {}'.format(e))
        return None


def get_robots_parser(robots_url):
    response = get_url_robots(robots_url)
    '''
    response = [x for x in response if 'Disallow:' in x]
    response = [x.replace('Disallow: ', '') for x in response]
    response = [x for x in response if x.count('/') > 1]
    '''
    return response

def try_reach_url(url, header):
    logs = dict()
    req = urllib.request.Request(url, data=None, headers=header)
    # Faking SSL certificate to avoid unauthorized requests
    gcontext = ssl._create_unverified_context()
    try:
        with urllib.request.urlopen(req, context=gcontext) as response:
            print('[{}] {}\n'.format(response.getcode(), url))
            logs.update({url: 'OK'})
    except urllib.error.HTTPError as e:
        if hasattr(e,'code'):
            print('[{}] UNABLE TO REACH URL : {}\n'.format(e.code, url))
        if hasattr(e,'reason'):
            print('Reason : {}\n'.format(e.reason))
        logs.update({url:e.reason})
    except urllib.error.URLError as e:
        print('Reason : {}\n'.format(e.reason))
        logs.update({url:e.reason})
    return logs

def get_url_robots(url, header):
    req = urllib.request.Request(url, data=None, headers=header)
    # Faking SSL certificate to avoid unauthorized requests
    gcontext = ssl._create_unverified_context()
    try:
        with urllib.request.urlopen(req, context=gcontext) as response:
            print('[{}] {}\n'.format(response.getcode(), url))
            return response.read().decode('utf-8', errors='ignore')#.split('\n')
    except (urllib.error.HTTPError, urllib.error.URLError) as e:
            return None
