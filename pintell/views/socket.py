import tornado
import time

from tornado.websocket import WebSocketHandler
from pintell.workers.live_view_worker import live_view
from pintell.utils import get_celery_task_state

class EchoWebSocket(WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        print('WebSocket opened')

    def on_message(self, message):
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

    def on_close(self):
        print('WebSocket closed')
        live_view.AsyncResult(self.message).revoke(terminate=True)
        print('Task ID {} stopped.'.format(self.message))
