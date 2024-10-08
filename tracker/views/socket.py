import tornado
import time
import json
from tornado.websocket import WebSocketHandler
from tracker.workers.live.live_view_worker import live_view
from tracker.workers.crawl_worker import link_crawler
from tracker.utils import get_celery_task_state

class EchoWebSocket(WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        print('WebSocket opened')

    def on_message(self, message):
        # '#' means it is a crawl task, otherwise it is live-view task
        if '#' in message:
            #print(' *** Crawl view ...')
            self.message = message
            #print('Message received = {}'.format(message))
            message = message.split('#')
            uid = message[0]
            task_id = message[1]
            #print('uid = {}, task_id = {}'.format(uid, task_id))
            task = link_crawler.AsyncResult(task_id)
            response = get_celery_task_state(task)
            #print('-> task response : {}'.format(response))
            if response['state'] == 'SUCCESS':
                #print('Task {} completed, sending socket order to close.'.format(task_id))
                self.write_message('<STOP>{}#{}'.format(uid, task_id))
            elif response['state'] == 'FAILURE':
                #print('Task {} FAILED, sending socket order to close.'.format(task_id))
                self.write_message('<STOP>{}#{}'.format(uid, task_id))
            else:
                try:
                    response['status']['uid'] = uid
                    #print('-> task response with uid : {}'.format(response))
                    self.write_message(response)
                except Exception as e:
                    # response['state'] == 'PENDING'
                    # print('still pending....')
                    self.write_message('<STOP_LIMIT>{}#{}'.format(uid, task_id))
        else:
            try:
                #print(' *** Live view ...')
                self.message = message
                # print('message = {}'.format(message))
                task_id = message
                task = live_view.AsyncResult(task_id)
                #print('Task backend = {}'.format(task.backend))
                #print('task_id: {}'.format(task_id))
                # print('TASL = {}'.format(task))

                # TODO: Catch ugly 
                # File "/usr/local/lib/python3.6/site-packages/tracker-0.0-py3.6.egg/tracker/utils.py", line 111, in get_celery_task_state
                #     'url': task.info.get('url'),
                # AttributeError: 'TimeLimitExceeded' object has no attribute 'get'
                # Maybe with :
                # if str(task.info).startswith('TimeLimitExceeded'):
                response = get_celery_task_state(task)
                response['task_id'] = task_id
                self.write_message(response)
            except Exception as e:
                # print('still pending....{}'.format(message))
                task = live_view.AsyncResult(task_id)
                self.write_message('<LIMIT_STOP>#{}'.format(task))
                # self.write_message(json.dumps({message: 'PENDING'}))


    def on_close(self):
        print('WebSocket closed')
        # if socket is used for a live view task, quit task on page close
        try:
            if '#' not in message:
                live_view.AsyncResult(self.message).revoke(terminate=True)
                print('Task ID {} stopped.'.format(self.message))
        except:
            pass