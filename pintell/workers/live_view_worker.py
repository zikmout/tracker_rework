import os
import time
import random
import celery
from celery import Celery
from pintell.celery import app_socket
import pintell.core.utils as utils
import pintell.core.scrapper as scrapper
import pintell.core.extractor as extractor

@app_socket.task(bind=True, ignore_result=False)
def live_view(self, links, base_path, diff_path, url):
    """ Try to download website parts that have changed """
    # VAL = [['/en/investors/stock-and-shareholder-corner/buyback-programs', ['DAILY DETAILS FOR THE PERIOD']]]
    #random.shuffle(links)
    total = len(links)
    i = 0
    for link in links:
        keywords = link[1]
        link = link[0]
        status = {
            'url': url + utils.find_internal_link(link),
            'div': url.split('//')[-1].split('/')[0],
            'diff_neg': None,
            'diff_pos': None,
            'nearest_link_pos': None,
            'diff_nb': 0
        }
        i += 1
        #time.sleep(random.randint(0, 10))
        base_dir_path = os.path.join(base_path, utils.find_internal_link(link).rpartition('/')[0][1:])
        filename = link.rpartition('/')[2]
        base_dir_path_file = os.path.join(base_dir_path, filename)

        # check whether adding 'unknown' is right ...
        if os.path.isdir(base_dir_path_file) and os.path.isfile(base_dir_path_file + 'unknown___'):
            base_dir_path_file = base_dir_path_file + 'unknown___'

        # getting local and remote content
        print('\n-> Fetching local content from : {}'.format(base_dir_path_file))
        print('-> Fetching remote content from : {}'.format(status['url']))
        local_content = scrapper.get_local_content(base_dir_path_file, 'rb')
        remote_content = scrapper.get_url_content(status['url'], header=utils.rh())

        if local_content is None or remote_content is None:
            print('Problem fetching local content or remote content.')
        else:
            status['diff_pos'], status['diff_neg'] = extractor.get_text_diff(local_content, remote_content)
            # if a list of keywords is provided, only get diff that matches keywords
            if keywords != []:
                match_neg, match_pos, nearest_link_pos = extractor.keyword_match(keywords, status['diff_neg'],
                    status['diff_pos'], remote_content, status['url'], url)
                status['diff_pos'] = match_pos
                status['diff_neg'] = match_neg
                if nearest_link_pos != []:
                    status['nearest_link_pos'] = [nearest_link_pos]
            self.update_state(state='PROGRESS', meta={'current': i, 'total': total, 'status': status})
            time.sleep(2)
            
            print('\n\n ({}) DIFF +++ :\n{}'.format(url, status['diff_pos']))
            print('\n\n ({}) DIFF --- :\n{}'.format(url, status['diff_neg']))
            #exit(0)
            if len(status['diff_pos']) > 0 or len(status['diff_neg']) > 0:
                print('***** Content is different *****')
                status['diff_nb'] += 1
            else:
                print('***** Content is SIMILAR *****')

    return {'current': 100, 'total': 100, 'status': status, 'result': status['diff_nb']}