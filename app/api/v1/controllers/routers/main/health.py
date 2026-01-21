from ....service.auth.rate_limit import RateLimiter
from fastapi import Request, Depends
from fastapi import APIRouter


router = APIRouter()

@router.get("/ping", dependencies=[Depends(RateLimiter(calls=20, period=60))])
async def ping(request: Request):
    return "Pong!"
