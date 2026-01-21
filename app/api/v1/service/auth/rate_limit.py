from fastapi import HTTPException, Request, status, Cookie
from .....config.middleware.redis import redis_client
from ...controllers.config.settings import settings

import jwt

def RateLimiter(calls: int = 10, period: int = 60):
    async def _dep(request: Request):
        client_ip = request.client.host if request.client else "unknown"
        key = f"rate_ip:{client_ip}"
        current = await redis_client.get(key)
        if current is None:
            await redis_client.setex(key, period, 1)
        elif int(current) >= calls:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="TOO_MANY_REQUESTS",
            )
        else:
            await redis_client.incr(key)
    return _dep


def rate_limit_user(calls: int = 20, period: int = 60):
    async def _dep(request: Request, access_token: str | None = Cookie(None)):
        if not access_token:
            return await RateLimiter(calls, period)(request)

        try:
            payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("sub")
            if not user_id:
                raise ValueError("missing sub")
        except Exception:
            return await RateLimiter(calls, period)(request)

        key = f"rate_user:{user_id}"
        current = await redis_client.get(key)
        if current is None:
            await redis_client.setex(key, period, 1)
        elif int(current) >= calls:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="TOO_MANY_REQUESTS",
            )
        else:
            await redis_client.incr(key)

    return _dep