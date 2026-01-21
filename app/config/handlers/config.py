from loguru import logger

import os

app_state_mode = os.getenv("MODE")

def configure_events(app):
    logger.remove()

    @app.on_event("startup")
    async def startup_event():
        logger.info("Application startup complete - FastAPI logger initialized")        