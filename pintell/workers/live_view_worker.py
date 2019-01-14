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

@app_socket.task(bind=True, ignore_result=False)
def live_view(self, links, base_path, diff_path, url):
    """ Try to download website parts that have changed """
    random.shuffle(links)
    nb_of_diff = 0
    total = len(links)
    i = 0
    for link in links:
        i += 1
        #time.sleep(random.randint(0, 10))
        base_dir_path = os.path.join(base_path, utils.find_internal_link(link).rpartition('/')[0][1:])
        filename = link.rpartition('/')[2]
        full_url = url + utils.find_internal_link(link)
        base_dir_path_file = os.path.join(base_dir_path, filename)
        if os.path.isdir(base_dir_path_file) and os.path.isfile(base_dir_path_file + '___'):
            base_dir_path_file = base_dir_path_file + '___'

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

            status = {
                'url': url + link,
                'div': url.split('//')[-1].split('/')[0],
                'diff_minus': extracted_diff_minus,
                'diff_plus': extracted_diff_plus
            }
            self.update_state(state='PROGRESS', meta={'current': i, 'total': total, 'status': status})

            print('\n\n DIFF +++ :\n{}'.format(extracted_diff_plus))
            print('\n\n DIFF --- :\n{}'.format(extracted_diff_minus))
            #exit(0)
            if len(extracted_diff_plus) > 1 or len(extracted_diff_minus) > 1:
                print('***** Content is different *****')
                nb_of_diff += 1
            else:
                print('***** Content is SIMILAR *****')

    return {'current': 100, 'total': 100, 'status': 'Taks Completed for website {}.'.format(url), 'result': nb_of_diff}