from fastapi import Request, HTTPException, status, Cookie, Response, Depends

from ......config.middleware.redis import redis_client
from ....service.auth.rate_limit import RateLimiter
from ...config.settings import settings
from fastapi import APIRouter

from ..user.login import create_access_token
from typing import Union


router = APIRouter()

@router.post("/refresh", dependencies=[Depends(RateLimiter(calls=15, period=60))])
async def refresh_token(
    request: Request,
    response: Response,
    refresh_token: str = Cookie(None),
) -> Union[dict, str]:
    COOKIE_SAMESITE = settings.COOKIE_SAMESITE
    COOKIE_SECURE = settings.COOKIE_SECURE
    COOKIE_DOMAIN = settings.COOKIE_DOMAIN

    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user_id = await redis_client.get(f"refresh:{refresh_token}")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    access_token = create_access_token(
        secret_key=str(settings.SECRET_KEY), user_id=str(user_id)
    )

    await redis_client.set(f"session:{access_token}", user_id, ex=60 * 15)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite=str(COOKIE_SAMESITE).lower(),
        domain=COOKIE_DOMAIN if COOKIE_DOMAIN else None,
        path="/",
        max_age=60 * 15,
    )

    return {
        "message": "Access token has been refreshed",
    }
