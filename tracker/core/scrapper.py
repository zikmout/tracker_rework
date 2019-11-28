import urllib
import urllib.request
import ssl
from ssl import SSLError
import time
import requests
from socket import timeout

# Taken from : https://codereview.stackexchange.com/questions/167327/scraping-the-full-content-from-a-lazy-loading-webpage
from pprint import pprint

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options as FirefoxOptions


class AdidasScraper:
    """ for website https://www.adidas-group.com/en/investors/investor-events/ only
    """
    def __init__(self, url):

        self.url = url
        # binary = FirefoxBinary('/Users/xxx/')
        # self.driver = webdriver.Firefox(firefox_binary=binary)
        options = FirefoxOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=options)

    def get_text_wait(self):#, max_company_count=1000):
        """Extracts and returns company links (maximum number of company links for return is provided)."""
        self.driver.implicitly_wait(10)
        self.driver.get(self.url)
        # Is this necessary ?
        # elements = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/article/section/div/section[2]')))
        html = self.driver.page_source
        # elements = self.driver.find_element_by_class_name("events future visible")
        # element = WebDriverWait(self.driver, 15).until(
        #     EC.presence_of_element_located((By.CLASS_NAME, "events future visible"))
        # )

        self.driver.quit()
        return html
        # last_line_number = 0
        # while last_line_number < max_company_count:
        #     self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        #     self.wait.until(lambda driver: self.get_last_line_number() != last_line_number)
        #     last_line_number = self.get_last_line_number()
        # return self.driver.find_elements_by_css_selector("ul.company-list > li > a")
        # return [company_link.get_attribute("href")
        #         for company_link in self.driver.find_elements_by_css_selector("ul.company-list > li > a")]

    # def get_company_data(self, company_link):
    #     """Extracts and prints out company specific information."""
    #     self.driver.get(company_link)

    #     return {
    #         row.find_element_by_css_selector(".company-info-card-label").text: row.find_element_by_css_selector(".company-info-card-data").text
    #         for row in self.driver.find_elements_by_css_selector('.company-info-card-table > .columns > .row')
    #     }

##############################################################################################

def get_url_content(url, header, verbose=True):
    """ Open remote website content
        args:
            url (str): Full url of remote content to access
            header (dict): Header to use when accessing content
        return:
            remote_content: Binary content decoded
    """
    error = None
    header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }
    # Faking User-Agent to avoid forbidden requests
    req = urllib.request.Request(url, data=None, headers=header)
    # Faking SSL certificate to avoid unauthorized requests
    gcontext = ssl._create_unverified_context()

    try:
        # download content of the url
        response = urllib.request.urlopen(req, context=gcontext, timeout=5)
        remote_content = response.read().decode('utf-8', errors='ignore')
    except (urllib.error.URLError, SSLError) as e:
        print('CATCHED SSL HANDSHAKE ERROR : {}'.format(e))
        print('Retrying HTTP request now ...\n')
        scraper = AdidasScraper(url)
        remote_content = scraper.get_text_wait()
        return remote_content, {url : '{}'.format(e)}

    except (timeout, TimeoutError) as e:
        print('[ERROR TIMEOUT] for url : {} (Error : {})'.format(url, e))
        # print('\n-------------> TIMEOUT ERROR CATCHED <----------------\n')
        print('Retrying HTTP request now ...\n')
        scraper = AdidasScraper(url)
        remote_content = scraper.get_text_wait()
        return remote_content, {url : '{}'.format(e)}

    except (urllib.error.HTTPError, ConnectionResetError, UnicodeDecodeError) as e:
        print('[ERROR] get_url_content : {}\n(url = {})'.format(e, url))
        return None, {url : '{}'.format(e)}
        #print('Return from scrapper2 =======>> {}'.format(remote_content))

    # if error is None:
    return remote_content, {url : ''}
    # Save content in the provided path with binary format

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