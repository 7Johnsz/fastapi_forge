from fastapi import Request, Depends
from fastapi import APIRouter


from ....service.auth.service import AuthService
from ....service.auth.rate_limit import RateLimiter

import psutil
import os


router = APIRouter()

@router.get("/memory", dependencies=[Depends(AuthService), Depends(RateLimiter(calls=20, period=60))])
async def memory(request: Request):
    process = psutil.Process(os.getpid())
    mem = process.memory_info()
    return {
        "memory": {
            "rss": mem.rss / (1024.0**3),
            "vms": mem.vms / (1024.0**3),
        }
    }
