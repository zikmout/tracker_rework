import os
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


broker = os.getenv('CELERY_BROKER_URL', 'amqp://guest@rabbitmq_server//')
backend = os.getenv('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')


download_worker_app = Celery(
    'download_worker',
    backend=backend,
    broker=broker,
)

crawl_worker_app = Celery(
    'crawl_worker',
    backend=backend,
    broker=broker,
)

live_view_worker_app = patch_celery().Celery('live_view',
                                             backend=backend,
                                             broker=broker,
                                             )
