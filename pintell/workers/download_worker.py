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
        time.sleep(2)
        if random_header:
            header = utils.rh()
        dir_path = os.path.join(base_path, utils.find_internal_link(link).rpartition('/')[0][1:])
        print('Saving file in {}'.format(dir_path))
        filename = link.rpartition('/')[2]
        print('Filename : {}\n\n'.format(filename))
        full_url = url + utils.find_internal_link(link)
        print('URL + LINK : {}'.format(full_url))
        if link.startswith('/'):
            download_and_save_content(full_url, filename, dir_path, header, check_duplicates=True)
        if link.startswith('<PDF>'):
            download_and_save_content(full_url, filename, dir_path, header)
        elif link.startswith('<EXCEL>'):
            # need to put function to download content for excel. Not called yet.
            print('EXCEL -> {}'.format(link))
        elif link.startswith('<ERROR>'):
            print('ERROR -> {}'.format(link))
    return {'current': 100, 'total': 100, 'status': 'Download task completed for website {}'.format(url), 'result': total}
'''
@app.task(bind=True, ignore_result=False)
def download(self, sender):
    ignore_result = False
    #sender = 'simsim'
    start = 1
    stop = 500
    total = stop - start
    for i in range(total):
        print('-> SENDER : {}, counter = {}'.format(sender, i))
        self.update_state(state='PROGRESS', meta={'current': i, 'total': total, 'status': 'sender{}'.format(i)})
        time.sleep(1)
    return {'current': 100, 'total': 100, 'status': 'Taks Completed for sender{}'.format(sender), 'result': 42}

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print ('Session Opened. IP:' + self.request.remote_ip)
        self.ioloop = tornado.ioloop.IOLoop.instance()
        self.send_websocket()

    def on_close(self):
        print("Session closed")

    def check_origin(self, origin):
        return True

    def send_websocket(self):
        self.ioloop.add_timeout(time.time() + 0.1, self.send_websocket)
        if self.ws_connection:
            message = json.dumps({
                'data1': random.randint(0, 100),
                'data2': random.randint(0, 100),
                })
            self.write_message(message)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/websocket', WebSocketHandler)
        ]
  
        settings = {
            'template_path': 'templates'
        }
        tornado.web.Application.__init__(self, handlers, **settings)
  
if __name__ == '__main__':
    ws_app = Application()
    server = tornado.httpserver.HTTPServer(ws_app)
    port = 8888
    server.listen(port)
    tornado.ioloop.IOLoop.instance().start()
    print ('[INFO] Tornado server for download_worker starts listening on port {}.!'.format(port))
'''