from celery import Celery

app = Celery('download_worker',
              backend='rpc://',
              broker='pyamqp://guest@localhost//',
             include=['pintell.workers'])