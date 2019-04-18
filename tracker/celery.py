from celery import Celery

download_worker_app = Celery('download_worker',
              backend='amqp://',
              broker='pyamqp://guest@localhost/')#,
             #include=['tracker.workers'])

crawl_worker_app = Celery('crawl_worker',
              backend='amqp://',
              broker='pyamqp://guest@localhost/')#,
             #include=['tracker.workers'])

live_view_worker_app = Celery('live_view',
              backend='amqp://',
              broker='pyamqp://guest@localhost/')#,
             #include=['tracker.workers'])