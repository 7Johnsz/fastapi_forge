from fastapi.responses import ORJSONResponse
from fastapi import FastAPI

# Configuration
from app.config.middleware.config import configure_middleware
from app.config.handlers.config import configure_events

# Router
from app.api.v1.controllers.routers.main import index

class BaseConfig:
    def __init__(self):
        self.app = FastAPI(
            description="Description of your API here",
            title="Title of your API",
            version="1.0.0",    
            default_response_class=ORJSONResponse)
    
    def create_app(self) -> FastAPI:
        # Configure app
        configure_middleware(self.app)
        configure_events(self.app)
        
        # Register routers
        self.app.include_router(index.router, tags=["Index"])
                
        return self.app

# Create application instance
base_config = BaseConfig()
app = base_config.create_app()