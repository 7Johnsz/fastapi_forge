from arq.connections import RedisSettings
from .base import startup, shutdown
from dotenv import load_dotenv

import os

load_dotenv(".env")

REDIS_QUEUE_HOST = os.getenv("REDIS_HOST") 
REDIS_QUEUE_PORT = int(os.getenv("REDIS_PORT") or 6379)
REDIS_QUEUE_PASSWORD = os.getenv("REDIS_PASSWORD")

print(f"Redis settings: {REDIS_QUEUE_HOST}:{REDIS_QUEUE_PORT} with password: {REDIS_QUEUE_PASSWORD}")

class WorkerSettings:
    """
    Worker settings for the Audiobook application.
    This class configures the worker with necessary settings and dependencies.
    """
    
    redis_settings = RedisSettings(
        host=REDIS_QUEUE_HOST,
        port=REDIS_QUEUE_PORT,
        password=REDIS_QUEUE_PASSWORD,
        database=0
    )
    on_startup = startup
    on_shutdown = shutdown
    functions = []