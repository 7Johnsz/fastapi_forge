from fastapi import Depends, Request, Response, HTTPException
from sqlmodel import select, Session
from loguru import logger
from typing import Union

from ....utils.token_gen import token_manager, create_access_token
from ......config.middleware.redis import redis_client
from ....service.auth.rate_limit import RateLimiter
from ...config.database.models.schema import Users
from ...config.database.config import get_session
from ...config.settings import settings
from ....models.Login import LoginModel
from fastapi import APIRouter


COOKIE_SAMESITE = settings.COOKIE_SAMESITE
COOKIE_SECURE = settings.COOKIE_SECURE
COOKIE_DOMAIN = settings.COOKIE_DOMAIN

router = APIRouter()

@router.post("/login", dependencies=[Depends(RateLimiter(calls=10, period=60))])
async def login(
    request: Request,
    response: Response,
    login_data: LoginModel,
    session: Session = Depends(get_session),
) -> Union[dict, str]:
    try:
        existing_user = session.exec(
            select(Users).where(Users.email == login_data.email)
        ).first()

        if not existing_user or not token_manager.decode(
            login_data.password, existing_user.password
        ):
            raise HTTPException(status_code=401, detail="INVALID_CREDENTIALS")

        access_token = create_access_token(
            str(existing_user.id), str(settings.SECRET_KEY)
        )
        refresh_token = token_manager.encode(str(existing_user.id))

        await redis_client.set(f"session:{access_token}", existing_user.id, ex=60 * 15)
        await redis_client.set(
            f"refresh:{refresh_token}", existing_user.id, ex=60 * 60 * 24 * 7
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=COOKIE_SECURE,
            samesite=str(COOKIE_SAMESITE).lower(),
            domain=COOKIE_DOMAIN if COOKIE_DOMAIN else None,
            path="/",
            max_age=60 * 60 * 24 * 7,
        )

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
            "message": "Login successful",
            "user": {
                "id": existing_user.id,
                "name": existing_user.name,
            },
        }

    except HTTPException:
        raise

    except Exception as e:
        logger.exception(f"Login failed for user attempt: {e}")
        raise HTTPException(status_code=500, detail="An error occurred during login")
