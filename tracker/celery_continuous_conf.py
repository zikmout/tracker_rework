broker_url = "redis://localhost:6379/5"
result_backend = "redis://localhost:6379/6"

# worker_pool = "eventlet"
# broker_pool_limit = 24

# add global limits to the tasks
task_annotations = {
	'cluster.add_task': {"rate_limit": "5/s"}
}

redbeat_redis_url = "redis://localhost:6379/7"

beat_scheduler = 'redbeat.RedBeatScheduler'
beat_max_loop_interval = 1

# timezone = 'Europe/Paris'

# enable_utc = False

beat_schedule = {}

# redbeat_lock_key = None