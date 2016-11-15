
import redis
import uuid
import time


def get_priority(priority=0):
    """
    Converts a typical integer priorty and produces a value that will incorporate time dimension
    such the value can be sorted so that older creation dates of similar priority sort first.

    :param priority: int, typical priorites are between 1-50
    :return: float
    """

class RedisQueueManager(object):
    """
    Manages redis priority queues that workers read.

    Queues are implemented with redis list, and priority is managed in a hash.
    """

    workqueue_q = 'workqueue:%s'
    running_q = 'worqueue:running:%s'
    priority_q = 'workqueue:pri:%s'

    aging_coef = 5*60  # seconds before a priority increases 1 integer (eg pri 1 --> 2 in N seconds, and 3 --> 4 in N sec)

    def __init__(self, server='localhost', port=6379, db=0):
        self._redis = redis.StringHost(server, port, db)


    def put_task(self, priority, topic, payload, task_id=None):
        task_id = task_id or uuid.uuid4().hex

        # 1. add task to priority hash add priority to current time to
        # 2. add task to workqueue
        self._redis.set(self.priority_q, task_id)

