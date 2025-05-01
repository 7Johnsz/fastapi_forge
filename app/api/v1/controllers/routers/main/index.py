from fastapi import Request

# Services
from ....service.auth.decorator import AuthService

# Config
from ......config.middleware.config import limiter
from ...config.api import router

@router.get("/")
@limiter.limit("30/minute")
@AuthService
async def root(request: Request):
    return "Hello World!"