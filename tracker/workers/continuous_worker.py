import time
from celery import Celery
from celery.schedules import crontab
# from celery.task import periodic_task
# from tracker.celery import continuous_tracking_worker_app
#from celery import shared_task
from celery.task.control import revoke

app = Celery('continuous_tracking_worker',
              backend='redis://',
              broker='redis://localhost:6379/2')#,

# continuous_tracking_worker_app.conf.timezone = 'Europe/London'
app.conf.redbeat_redis_url = "redis://localhost:6379/2"

@app.task(bind=True)
def add_task(self, x, y):
	print('Addition = {}'.format(x+y))
	return x+y

# @continuous_tracking_worker_app.on_after_configure.connect
# @continuous_tracking_worker_app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
# 	print('OKI inside setup periodic tasks ...')
# 	task_id = sender.add_periodic_task(10.0, test.s('Simon'), name='add every 10')
# 	print('RET = {}'.format(task_id))
	#print('Prepare to sleep for 60 seconds ...')
	#time.sleep(60)
	#print('End sleeping, waking up to stop task ! Del from DICT ;)')
	#print('beat_schedule = {}'.format(continuous_tracking_worker_app.conf.beat_schedule))
	#del continuous_tracking_worker_app.conf.beat_schedule['add every 10']

# @continuous_tracking_worker_app.task
# def test(name):
# 	print('Periodic task called, name = {}'.format(name))

#@periodic_task(run_every=(crontab(minute='*/1')), name="task-hello")
# @periodic_task(run_every=(crontab(minute='*/1')), name="task-hello")
# def print_hello(name):
#     print('Hello World! ---> {}'.format(name))

# @shared_task
# def add(a, b):
#     print(a + b)

# @shared_task
# def mul(a, b):
#     print(a * b)