from loguru import logger

import redis.asyncio as redis
import os

redis_host = os.getenv("REDIS_HOST")
redis_port = int(os.getenv("REDIS_PORT"))
redis_password = os.getenv("REDIS_PASSWORD")

redis_pool = redis.ConnectionPool(
    host=redis_host,
    password=redis_password,
    port=redis_port,
    decode_responses=True,  
    db=0)

redis_client = redis.Redis(connection_pool=redis_pool)

redis_pool_bytes = redis.ConnectionPool(
    host=redis_host,
    password=redis_password,
    port=redis_port,
    decode_responses=False,  
    db=0)

redis_bytes_client = redis.Redis(connection_pool=redis_pool_bytes)

async def redis_connection():
    try:
        await redis_client.ping()
        await redis_bytes_client.ping()
        logger.info("Connected to Redis successfully")
    except redis.ConnectionError as e:
        raise RuntimeError(f"Redis connection error: {e}")