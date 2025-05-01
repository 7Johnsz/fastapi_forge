from scalar_fastapi import get_scalar_api_reference
from fastapi import Request

# Services
from ....service.auth.decorator import AuthService

# Config
from .....config.middleware.config import limiter
from ...config.api import router

import psutil
import os

@router.get("/")
@limiter.limit("30/minute")
@AuthService
async def root(request: Request):
    return "Hello World!"

@router.get("/ping")
@limiter.limit("30/minute")
async def ping(request: Request):
    return "Pong!"

@router.get("/memory")
@limiter.limit("30/minute")
@AuthService
async def memory(request: Request):
    process = psutil.Process(os.getpid())
    mem = process.memory_info()
    return {
        "memory": {
            "rss": mem.rss / (1024.0 ** 3),  
            "vms": mem.vms / (1024.0 ** 3), 
        }
    }

@router.get("/scalar", include_in_schema=False)
@limiter.limit("30/minute")
@AuthService
async def scalar_html(request: Request):
    return get_scalar_api_reference(
        openapi_url=request.app.openapi_url,
        title=request.app.title)