from app.api.v1.controllers.config.settings import settings
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

import sentry_sdk

redis_password = settings.REDIS_PASSWORD
redis_host = settings.REDIS_HOST
redis_port = settings.REDIS_PORT

ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3009",
]


def configure_middleware(app):
    """
    Configure the FastAPI application with various middlewares.

    This function sets up the application with the following middlewares:

    - GZipMiddleware: A middleware to compress responses larger than 1000 bytes.
    - CORSMiddleware: A middleware to enable CORS on the application.

    :param app: The FastAPI application instance.
    """
    if settings.API_MODE == "production":
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN, send_default_pii=True, traces_sample_rate=1.0
        )

    app.add_middleware(GZipMiddleware, minimum_size=1000, compresslevel=5)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["*"],
        expose_headers=["*"],
    )
