import os
import time
import celery
from celery import Celery
from pintell.celery import app_socket

@app_socket.task(bind=True, ignore_result=False)
def live_view(self):
    ignore_result = False
    sender = 'simsim'
    start = 1
    stop = 500
    total = stop - start
    for i in range(total):
        print('-> SENDER : {}, counter = {}'.format(sender, i))
        self.update_state(state='PROGRESS', meta={'current': i, 'total': total, 'status': 'sender{}'.format(i)})
        time.sleep(1)
    return {'current': 100, 'total': 100, 'status': 'Taks Completed for sender{}'.format(sender), 'result': 42}