import celery
from celery import Celery
from pintell.celery import app
import json
import time
import random
import tornado.websocket
import tornado.web
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop

@app.task(bind=True)
def download(self, sender):
	#sender = 'simsim'
	start = 1
	stop = 500
	total = stop - start
	for i in range(total):
		print('-> SENDER : {}, counter = {}'.format(sender, i))
		self.update_state(state='PROGRESS', meta={'current': i, 'total': total, 'status': 'sender{}'.format(i)})
		time.sleep(1)
	return {'current': 100, 'total': 100, 'status': 'Taks Completed for sender{}'.format(sender), 'result': 42}

'''
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