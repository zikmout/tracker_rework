import re
import ssl
import time
import datetime
import urllib.request
from urllib import robotparser
from urllib.parse import urljoin
from urllib.error import URLError, HTTPError, ContentTooShortError
import tracker.core.utils as utils

nb_errors = 0
pages = set()
links = set()
files = set()
full_links = set()
gcontext = ssl._create_unverified_context()

def get_pdf_excel_links(files):
    pdfs = list()
    excels = list()

    for link in files:
        if link is None:
            pass
        elif link.endswith('pdf') or link.endswith('PDF') or '.PDF' in link \
                or '.pdf' in link:
            pdfs.append(link)
        elif link.endswith('xls') or link.endswith('xlsx') \
                or link.endswith('XLS') or link.endswith('XLSX'):
            excels.append(link)
    return pdfs, excels

def is_valid_content_type(url, content_type):
    to_exclude = ['audio', 'image', 'None']
    to_include = ['html']
    for _ in to_include:
        if _ in content_type:
            return True
    for _ in to_exclude:
        if _ in content_type:
            return False
    return True

def is_valid_link(link):
    exclude_contains = ['.jpg', '.jpeg', '.png', '.wmv', '.ics', '.mp3', '.zip',\
     '.rtf', '.mov', '.mp4', '.m4a', '.mpg', '@', '.doc', '#', ';', 'amp%3B', '.gif', '.vcf',\
     '.exe', '.xml', '&amp', '.tif', '.JPG', '.pptx', '.ppt']
     #'=http%3A%2F%2F', '=http://', '=https%3A%2F%2F', '=https://']
    for _ in exclude_contains:
        if _ in link:
            return False
    if link.endswith('pdf') or link.endswith('PDF') or '.PDF' in link \
            or '.pdf' in link:
        return False
    if link.endswith('xls') or link.endswith('xlsx') \
            or link.endswith('XLS') or link.endswith('XLSX'):
        return False
    return True

def download(start_url, url, num_retries=2, user_agent='wswp', charset='utf-8', proxy=None):
    """ Download a given URL and return the page content
        args:
            start_url(str): URL with http:// ...
            url (str): URI (ex: /finance)
        kwargs:
            user_agent (str): user agent (default: wswp)
            charset (str): charset if website does not include one in headers
            proxy (str): proxy url, ex 'http://IP' (default: None)
            num_retries (int): number of retries if a 5xx error is seen (default: 2)
    """
    print('\ndownload : url = {}'.format(url))
    err = 0
    subfiles = None
    subpages = None
    request = urllib.request.Request(url)
    request.add_header('User-agent', utils.ua())
    try:
        end_url = url.replace(start_url, '')
        '''
        if proxy:
            proxy_support = urllib.request.ProxyHandler({'http': proxy})
            opener = urllib.request.build_opener(proxy_support)
            urllib.request.install_opener(opener)
        '''
        resp = urllib.request.urlopen(request, context=gcontext)
        cs = resp.headers.get_content_charset()
        #cs = resp.headers.get_content_charset()
        if not cs:
            cs = charset
        info = resp.info()
        cs2 = info.get_content_type()
        is_valid = is_valid_link(url)
        check = 0
        if 'pdf' in cs2:
            subfiles = '<PDF> ' + end_url
            print('<PDF> {}'.format(end_url))
            check += 1
        elif 'excel' in cs2:
            subfiles = '<EXCEL> ' + end_url
            print('<EXCEL> {}'.format(end_url))
            check += 1
        elif is_valid and not end_url.startswith('http'):
            print(end_url)
            subpages = end_url
        if is_valid_content_type(url, cs2) and is_valid and not check:
            try :
                html = resp.read().decode('utf-8')
            except Exception as e:
                print('Error ({}) --> {}'.format(end_url, e))
                html = None
        else:
            html = None
    except (URLError, HTTPError, ContentTooShortError, UnicodeEncodeError) as e:
        #print('<ERROR> {} ({})'.format(e, url))
        #print('Download error:', e.reason)
        html = None
        err += 1
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # recursively retry 5xx HTTP errors
                return download(start_url, url, num_retries - 1)
    return html, subpages, subfiles, err


def get_robots_parser(robots_url):
    """ Return the robots parser object using the robots_url """
    rp = robotparser.RobotFileParser()
    rp.set_url(robots_url)
    rp.read()
    return rp


def get_links(start_url, html):
    " Return a list of links (using simple regex matching) from the html content "
    # a regular expression to extract all links from the webpage
    webpage_regex = re.compile("""<a[^>]+href=["'](.*?)["']""", re.IGNORECASE)
    links = webpage_regex.findall(html)
    
    links2 = list()
    for link in links:
        if link.startswith(start_url):
            link = link.replace(start_url, '')
        links2.append(link)
    return links2

def link_crawler(start_url, link_regex, robots_url=None, user_agent='wswp',
                 proxy=None, delay=3, max_depth=1):
    """ Crawl from the given start URL following links matched by link_regex. In the current
        implementation, we do not actually scrapy any information.

        args:
            start_url (str): web site to start crawl
            link_regex (str): regex to match for links
        kwargs:
            robots_url (str): url of the site's robots.txt (default: start_url + /robots.txt)
            user_agent (str): user agent (default: wswp)
            proxy (str): proxy url, ex 'http://IP' (default: None)
            delay (int): seconds to throttle between requests to one domain (default: 3)
            max_depth (int): maximum crawl depth (to avoid traps) (default: 4)
    """
    global nb_errors
    global pages
    global files
    global full_links

    nb_errors = 0
    start_time = time.time()
    crawl_queue = [start_url]
    # keep track which URL's have seen before
    seen = {}
    #if not robots_url:
    #    robots_url = '{}/robots.txt'.format(start_url)
    #rp = get_robots_parser(robots_url)
    while crawl_queue:
        url = crawl_queue.pop()
        # check url passes robots.txt restrictions
        #if rp.can_fetch(user_agent, url):
        depth = seen.get(url, 0)
        if depth == max_depth:
            print('*** Skipping {} due to depth ***'.format(url))
            continue
        html, subpages, subfiles, err = download(start_url, url, user_agent=user_agent, proxy=proxy)
        pages.add(subpages)
        files.add(subfiles)
        nb_errors += err
        if not html:
            continue
        # TODO: add actual data scraping here
        # filter for links matching our regular expression
        for link in get_links(start_url, html):
            #print('sublink ------> {}'.format(link))
            if re.match(link_regex, link):
                abs_link = urljoin(start_url, link)
                if abs_link not in seen:
                    seen[abs_link] = depth + 1
                    crawl_queue.append(abs_link)

    # ideally None(s) had to be removed from above !
    #pages |= full_links
    files = list(filter(None, files))
    pages = list(filter(None, pages))
    total_pages = len(pages) + len(files) + nb_errors
    pdfs, excels = get_pdf_excel_links(files)
    end_time = time.time()
    elapsed_time = end_time - start_time
    log = '\n[{}] Duration: {} / Total: {} / Page(s): {} / PDF(s): {} / EXCEL(s): {} / Errors: {}'.format(\
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),\
         total_pages, len(pages), len(pdfs), len(excels), nb_errors)
    return pages, files, log
        #else:
        #    print('Blocked by robots.txt:', url)