import os
import time
import celery
from celery import Celery
from pintell.celery import app
from pintell.core.downloader import download_and_save_content
import pintell.core.utils as utils

@app.task(bind=True)
def download_website(self, links, base_path, url, random_header=False):
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
        self.update_state(state='PROGRESS', meta={'current': counter, 'total': total, 'status': '{}'.format(link)})
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
    return {'current': 100, 'total': 100, 'status': 'Download task completed for website {}'.format(url), 'result': total}
