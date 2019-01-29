from celery import Celery

app = Celery('download_worker',
              backend='amqp://',
              broker='pyamqp://guest@localhost/',
             include=['tracker.workers'])

app_socket = Celery('live_view',
              backend='amqp://',
              broker='pyamqp://guest@localhost/',
             include=['tracker.workers'])