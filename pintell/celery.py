from celery import Celery

app = Celery('download_worker',
              backend='amqp://',
              broker='pyamqp://guest@localhost//',
             include=['pintell.workers'])