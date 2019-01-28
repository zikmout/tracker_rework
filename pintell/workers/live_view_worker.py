import os
import time
import random
import celery
from celery import Celery
from pintell.celery import app_socket
import pintell.core.utils as utils
import pintell.core.scrapper as scrapper
import pintell.core.extractor as extractor
from pintell.core.downloader import clean_content
import lxml.html as LH
import itertools

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

@app_socket.task(bind=True, ignore_result=False)
def live_view(self, links, base_path, diff_path, url):
    """ Try to download website parts that have changed """
    # VAL = [['/en/investors/stock-and-shareholder-corner/buyback-programs', ['DAILY DETAILS FOR THE PERIOD']]]
    #random.shuffle(links)
    nb_of_diff = 0
    total = len(links)
    i = 0
    for link in links:
        keywords = link[1]
        link = link[0]
        status = {
            'url': url + link,
            'div': url.split('//')[-1].split('/')[0],
            'diff_minus': None,
            'diff_plus': None
        }
        i += 1
        #time.sleep(random.randint(0, 10))
        base_dir_path = os.path.join(base_path, utils.find_internal_link(link).rpartition('/')[0][1:])
        filename = link.rpartition('/')[2]
        full_url = url + utils.find_internal_link(link)
        base_dir_path_file = os.path.join(base_dir_path, filename)
        # check whether adding 'unknown' is right ...
        if os.path.isdir(base_dir_path_file) and os.path.isfile(base_dir_path_file + 'unknown___'):
            base_dir_path_file = base_dir_path_file + 'unknown___'

        # getting local file content
        print('\n-> Opening base_dir_path_file = {}'.format(base_dir_path_file))

        local_content = scrapper.get_local_content(base_dir_path_file, 'rb')
        if local_content is None:
            print('Problem fetching local content')
        else:
            # getting full_url content
            print('-> Getting content of webpage to compare : {}'.format(full_url))
            
            remote_content = scrapper.get_url_content(full_url, header=utils.rh())

            extracted_local_content = extractor.extract_text_from_html(local_content)
            extracted_local_content = clean_content(extracted_local_content)
            extracted_remote_content = extractor.extract_text_from_html(remote_content)
            extracted_remote_content = clean_content(extracted_remote_content)

            #print('REMOTE CONTENT = {}\n'.format(remote_content))

            extracted_diff_minus = [x for x in extracted_local_content if x not in extracted_remote_content]
            extracted_diff_plus = [x for x in extracted_remote_content if x not in extracted_local_content]
            
            check = []
            if keywords != []:
                print('keywords = {}'.format(keywords))
                print('Filtering ....')
                filtered_diff_minus = list()
                filtered_diff_plus = list()
                for keyword in keywords:
                    for minus in extracted_diff_minus:
                        if keyword in minus:
                            filtered_diff_minus.append(minus)
                    for plus in extracted_diff_plus:
                        if keyword in plus:
                            print('********** KEYWORD {} FOUND on url {}'.format(keyword, full_url))
                            filtered_diff_plus.append(plus)
                            doc = LH.fromstring(remote_content)
                            xpaths = doc.xpath('//*[contains(text(),{s!r})]'.format(s = keyword))
                            len_xpaths = len(xpaths)
                            for x in xpaths:
                                check = find_nearest(x)
                                if check.startswith(url) is False:
                                    check = url + check
                                print('Nearsest found = {}'.format(check))
                                if len_xpaths > 1:
                                    print('Nearest founds are numerous for website : {}. Exit.'.format(full_url))
                                    break ;

                status['diff_plus'] = filtered_diff_plus
                status['diff_minus'] = filtered_diff_minus
                if check != []:
                    status['diff_plus'] += [check]
            else:
                status['diff_plus'] = extracted_diff_plus
                status['diff_minus'] = extracted_diff_minus

            self.update_state(state='PROGRESS', meta={'current': i, 'total': total, 'status': status})
            time.sleep(1)
            print('\n\n DIFF +++ :\n{}'.format(extracted_diff_plus))
            print('\n\n DIFF --- :\n{}'.format(extracted_diff_minus))
            #exit(0)
            if len(extracted_diff_plus) > 1 or len(extracted_diff_minus) > 1:
                print('***** Content is different *****')
                nb_of_diff += 1
            else:
                print('***** Content is SIMILAR *****')

    return {'current': 100, 'total': 100, 'status': 'Taks Completed for website {}.'.format(url), 'result': nb_of_diff}