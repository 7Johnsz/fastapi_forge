from fastapi import Response, Cookie, Depends

from ....service.auth.rate_limit import RateLimiter

from ......config.middleware.redis import redis_client
from ...config.settings import settings
from fastapi import APIRouter


router = APIRouter()

COOKIE_SAMESITE = settings.COOKIE_SAMESITE
COOKIE_SECURE = settings.COOKIE_SECURE
COOKIE_DOMAIN = settings.COOKIE_DOMAIN

@router.post("/logout", dependencies=[Depends(RateLimiter(calls=20, period=60))])
async def logout(
    response: Response,
    access_token: str | None = Cookie(None),
    refresh_token: str | None = Cookie(None),
) -> dict:
    try:
        if access_token:
            await redis_client.delete(f"session:{access_token}")
        if refresh_token:
            await redis_client.delete(f"refresh:{refresh_token}")
    except Exception:
        pass

    response.delete_cookie(
        "refresh_token",
        httponly=True,
        samesite=str(COOKIE_SAMESITE).lower(),
        domain=COOKIE_DOMAIN if COOKIE_DOMAIN else None,
        path="/",
    )
    response.delete_cookie(
        "access_token",
        httponly=True,
        samesite=str(COOKIE_SAMESITE).lower(),
        domain=COOKIE_DOMAIN if COOKIE_DOMAIN else None,
        path="/",
    )

    return {"message": "Logout successful"}
