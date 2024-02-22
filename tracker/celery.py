import celery
from celery import Celery, group, states
from celery.backends.redis import RedisBackend


def patch_celery():
    """Patch redis backend."""

    def _unpack_chord_result(
        self, tup, decode,
        EXCEPTION_STATES=states.EXCEPTION_STATES,
        PROPAGATE_STATES=states.PROPAGATE_STATES,
    ):
        _, tid, state, retval = decode(tup)

        if state in EXCEPTION_STATES:
            retval = self.exception_to_python(retval)
        if state in PROPAGATE_STATES:
            # retval is an Exception
            return '{}: {}'.format(retval.__class__.__name__, str(retval))

        return retval

    celery.backends.redis.RedisBackend._unpack_chord_result = _unpack_chord_result

    return celery


download_worker_app = Celery('download_worker',
                             backend='amqp://',
                             broker='pyamqp://guest@localhost/')  # ,
# include=['tracker.workers'])

crawl_worker_app = Celery('crawl_worker',
                          backend='amqp://',
                          broker='pyamqp://guest@localhost/')  # ,
# include=['tracker.workers'])

# include=['tracker.workers'])
# live_view_worker_app2 = patch_celery().Celery('live_view2',
#               backend='amqp://',
#               broker='pyamqp://guest@localhost/')#,

# live_view_worker_app2.conf.update(
# result_expires=999600,
# )

# live_view_worker_app = patch_celery().Celery('live_view',
#                                              backend='amqp://',
#                                              broker='pyamqp://guest@localhost/')  # ,

live_view_worker_app = patch_celery().Celery('live_view',
                                             backend='amqp://',
                                             broker='redis://localhost:6379/1')  # ,

# app = Celery(__name__) # TODO : Change to sth like 'permanent listener'
# app.config_from_object(celeryconf)
# continuous_tracking_worker_app = Celery('continuous_tracking_worker',
#               backend='amqp://',
#               broker='redis://localhost:6379/1')#,
# include=['tracker.workers'])
