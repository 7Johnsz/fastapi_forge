from arq.worker import Worker
from loguru import logger
from ....config.middleware.redis import redis_client, redis_bytes_client

async def startup(ctx: Worker) -> None:
    logger.info("Worker Started")
    
    try:
        await redis_client.ping()
        await redis_bytes_client.ping()
        logger.info("Redis clients connected successfully")
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")

async def shutdown(ctx: Worker) -> None:
    logger.info("Worker end")