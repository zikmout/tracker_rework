"""

"""
import celery
import tracker.celery_continuous_conf as celeryconf
import uuid

app = celery.Celery(__name__)
app.config_from_object(celeryconf)

@app.task(bind=True)
def test_task(self, x):
	return x

@app.task(bind=True)
def print_task(self, x):
	print('PRINT TASK, ret = {}'.format(x))
	return x

# if , throw=True, execute the task after worker restart, not at next schedule
@app.task(bind=True, requeue=False, retry=False)
def add_task(self, x, y):
	print('ADD TASK, ret = {}'.format(x+y))
	return x+y

@app.task(bind=True)
def bad_task(self):
	raise RuntimeError("intentional error")


@app.task(bind=True)
def chaining_task(self, add):
	return celery.chain(add_task.s(*add), print_task.s()).apply_async()

# you can do this from a separate threads
#from redbeat import RedBeatSchedulerEntry as Entry
# e = Entry(
# 	'thingo',
# 	'cluster.chaining_task',
# 	10,
# 	args=([5, 6], ),
# 	options={'schedule_id': 'testid'},
# 	app=app)
# e.save()
#print('DICT = {}'.format(Entry))
#e = Entry.from_key('592')
#e.delete()





