from arq.connections import RedisSettings
from arq import create_pool

import os

REDIS_QUEUE_HOST = os.getenv("REDIS_HOST")
REDIS_QUEUE_PORT = int(os.getenv("REDIS_PORT"))
REDIS_QUEUE_PASSWORD = os.getenv("REDIS_PASSWORD")

enqueue_pool = RedisSettings(
    host=REDIS_QUEUE_HOST,
    port=REDIS_QUEUE_PORT,
    password=REDIS_QUEUE_PASSWORD,
    database=0
)

_redis_pool = None

async def get_redis_pool():
    global _redis_pool
    if not _redis_pool:
        _redis_pool = await create_pool(enqueue_pool)
    return _redis_pool

async def send_queue(task_name: str, task_data):
    redis = await get_redis_pool()
    return await redis.enqueue_job(task_name, task_data)