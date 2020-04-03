broker_url = "redis://localhost:6379/5"
result_backend = "redis://localhost:6379/6"

# worker_pool = "eventlet"
# broker_pool_limit = 24

# beat_max_loop_interval 5 #?? duplicate tasks ?
#CELERY_ALWAYS_EAGER=False

# add global limits to the tasks
task_annotations = {
	'continuous_worker.get_diff': {"rate_limit": "5/s"}
}

redbeat_redis_url = "redis://localhost:6379/7"

beat_scheduler = 'redbeat.RedBeatScheduler'
beat_max_loop_interval = 1

# timezone = 'Europe/Paris'

# enable_utc = False

beat_schedule = {}

# redbeat_lock_key = None