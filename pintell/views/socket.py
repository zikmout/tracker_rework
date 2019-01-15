import tornado
import time
from tornado.websocket import WebSocketHandler
from pintell.workers.live_view_worker import live_view
from pintell.workers.crawl_worker import link_crawler
from pintell.utils import get_celery_task_state

class EchoWebSocket(WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        print('WebSocket opened')

    def on_message(self, message):
        if '#' in message:
            print(' *** Crawl view ...')
            self.message = message
            print('Message received = {}'.format(message))
            message = message.split('#')
            uid = message[0]
            task_id = message[1]
            print('uid = {}, task_id = {}'.format(uid, task_id))
            task = link_crawler.AsyncResult(task_id)
            response = get_celery_task_state(task)
            print('-> task response : {}'.format(response))
            try:
                response['status']['uid'] = uid
                print('-> task response with uid : {}'.format(response))
                self.write_message(response)
            except Exception as e:
                print('still pending....')
        else:
            print(' *** Live view ...')
            '''
            self.message = message
            print('message = {}'.format(message))
            #self.write_message(u"You said: " + message)
            task_id = message
            task = live_view.AsyncResult(task_id)
            print('Task backend = {}'.format(task.backend))
            #task = task.get()
            print('task_id: {}'.format(task_id))
            response = get_celery_task_state(task)
            self.write_message(response)
            '''

    def on_close(self):
        print('WebSocket closed')
        '''
        live_view.AsyncResult(self.message).revoke(terminate=True)
        print('Task ID {} stopped.'.format(self.message))
        '''
