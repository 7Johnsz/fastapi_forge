from fastapi import Request, Depends

# Services
from ....service.auth.service import AuthService
from ....service.auth.rate_limit import RateLimiter

from fastapi import APIRouter


router = APIRouter()

@router.get("/", dependencies=[Depends(AuthService), Depends(RateLimiter(calls=20, period=60))])
async def root(request: Request):
    return "Hello World!"
