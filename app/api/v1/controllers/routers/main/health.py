from fastapi import Request

# Config
from ......config.middleware.config import limiter
from ...config.api import router

@router.get("/ping")
@limiter.limit("30/minute")
async def ping(request: Request):
    return "Pong!"