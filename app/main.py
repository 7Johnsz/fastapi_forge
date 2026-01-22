from app.api.v1.controllers.routers.user.signup import signup
from fastapi.responses import ORJSONResponse
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.v1.controllers.config.database.config import Database
from app.config.middleware.config import configure_middleware
from app.config.middleware.redis import redis_connection
from .api.v1.controllers.config.settings import settings
from app.config.handlers.config import configure_events
from app.api.v1.utils.logging import setup_logger

from app.api.v1.controllers.routers.main import index, memory, health, docs
from app.api.v1.controllers.routers.security import refresh_token
from app.api.v1.controllers.routers.user import login, logout


class BaseConfig:
    def __init__(self):
        if settings.API_MODE == "development":
            self.app = FastAPI(
                description="FastAPI Forge is a boilerplate for FastAPI applications.",
                version="1.0.1",
                default_response_class=ORJSONResponse,
                lifespan=self.lifespan,
            )
        else:
            self.app = FastAPI(
                description="FastAPI Forge is a boilerplate for FastAPI applications.",
                title="FastAPI Forge Backend API",
                version="1.0.1",
                default_response_class=ORJSONResponse,
                lifespan=self.lifespan,
                docs_url=None,
                redoc_url=None,
                openapi_url=None,
            )

    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        print("Starting up...")
        try:
            Database()
            await redis_connection()

            yield
        finally:
            print("Shutting down...")

    def create_app(self) -> FastAPI:
        # Configure app
        configure_middleware(self.app)
        configure_events(self.app)

        # Main routers
        self.app.include_router(health.router, tags=["Main"])
        self.app.include_router(memory.router, tags=["Main"])
        self.app.include_router(index.router, tags=["Main"])
        self.app.include_router(docs.router, tags=["Main"])

        # User routers
        self.app.include_router(signup.router, tags=["User"])
        self.app.include_router(logout.router, tags=["User"])
        self.app.include_router(login.router, tags=["User"])

        # Security routers
        self.app.include_router(refresh_token.router, tags=["Security"])

        logger = setup_logger()

        @self.app.middleware("http")
        async def log_requests(request, call_next):
            logger.debug(f"Request: {request.method} {request.url}")
            response = await call_next(request)
            logger.debug(f"Response: {response.status_code}")
            return response

        return self.app


base_config = BaseConfig()
app = base_config.create_app()