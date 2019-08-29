from celery import Celery

# CELERY_TIMEZONE = 'Europe/London'

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

# continuous_tracking_worker_app = Celery('continuous_tracking_worker',
#               backend='amqp://',
#               broker='redis://localhost:6379/1')#,
             #include=['tracker.workers'])