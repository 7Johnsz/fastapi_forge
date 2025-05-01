from loguru import logger
import time
import sys
from contextlib import asynccontextmanager

def configure_events(app):
    logger.remove()
    logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | {level} | <cyan>{message}</cyan>",
        level="DEBUG"
    )

    @asynccontextmanager
    async def lifespan(app):
        start_time = time.time()
        logger.info("Starting application initialization...")
        logger.info("Initializing middleware...")
        logger.info("Initializing routes...")
        logger.info("Initializing services...")
        yield
        end_time = time.time()
        logger.info(f"Application started in {end_time - start_time} seconds")

    app.router.lifespan_context = lifespan