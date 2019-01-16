import os
import time
import datetime
import random
from urllib.parse import urljoin
import re
import celery
from celery import Celery
from pintell.celery import app_socket
import pintell.core.crawler as crawler
import pintell.core.logger as logger

#import celery.bin.amqp
#amqp = celery.bin.amqp.amqp(app = app_socket)
#amqp.run('queue.purge', '2')

nb_errors = 0
pages = set()
links = set()
files = set()
full_links = set()

@app_socket.task(bind=True, ignore_result=False)
def link_crawler(self, start_url, link_regex, logfile, user_agent, max_depth, robots_url=None, proxy=None, delay=3):
    print('MAX DEPTH RECEIVED === {}'.format(max_depth))
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

    log_debut = '[{}] {}\n'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), start_url)
    nb_errors = 0
    start_time = time.time()
    crawl_queue = [start_url]
    # keep track which URL's have seen before
    seen = {}
    #if not robots_url:
    #    robots_url = '{}/robots.txt'.format(start_url)
    #rp = get_robots_parser(robots_url)
    i = 0
    while crawl_queue:
        total = len(crawl_queue)
        i += 1
        url = crawl_queue.pop()
        # check url passes robots.txt restrictions
        #if rp.can_fetch(user_agent, url):
        depth = seen.get(url, 0)
        print('seen depth (max = {})----> {}'.format(max_depth, depth))
        if depth >= int(max_depth):
            print('*** Skipping {} due to depth ***'.format(url))
            continue
        html, subpages, subfiles, err = crawler.download(start_url, url, user_agent=user_agent, proxy=proxy)
        pages.add(subpages)
        files.add(subfiles)
        nb_errors += err
        if not html:
            continue
        # TODO: add actual data scraping here
        # filter for links matching our regular expression
        for link in crawler.get_links(start_url, html):
            if re.match(link_regex, link):
                abs_link = urljoin(start_url, link)
                if abs_link not in seen:
                    seen[abs_link] = depth + 1
                    crawl_queue.append(abs_link)
                lnk = abs_link
            else:
                lnk = link
            status = {
                'link': link,
                'div': start_url.split('//')[-1].split('/')[0]
            }
            self.update_state(state='PROGRESS', meta={'current': i, 'total': total, 'status': status})
    # ideally None(s) had to be removed from above !
    files = list(filter(None, files))
    pages = list(filter(None, pages))
    total_pages = len(pages) + len(files) + nb_errors
    pdfs, excels = crawler.get_pdf_excel_links(files)
    end_time = time.time()
    elapsed_time = end_time - start_time
    log_fin = '\n[{}] Duration: {} / Total: {} / Page(s): {} / PDF(s): {} / EXCEL(s): {} / Errors: {}'.format(\
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),\
         total_pages, len(pages), len(pdfs), len(excels), nb_errors)
    # save logs into logfile
    logger.save_urls(logfile, pages, files, log_debut, log_fin)
    return {'current': 100, 'total': 100, 'status': 'Crawling task Completed for website {}.'.format(start_url), 'result': total_pages}