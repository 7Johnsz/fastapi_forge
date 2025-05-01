from fastapi import Request

# Config
from ......config.middleware.config import limiter
from ...config.api import router

# Services
from ....service.auth.decorator import AuthService

import psutil
import os

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