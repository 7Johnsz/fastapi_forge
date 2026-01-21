from fastapi import Depends, Request, BackgroundTasks, Response
from fastapi.exceptions import HTTPException

from ...config.database.models.schema import Users
from ...config.database.config import get_session
from ...config.settings import settings
from fastapi import APIRouter


from ....utils.token_gen import token_manager, create_access_token
from ......config.middleware.redis import redis_client
from ....service.auth.rate_limit import RateLimiter
from ....utils.encodehost import encode_host
from ....utils.get_ip import get_real_ip
from ....models.User import UserModel

from sqlmodel import select, Session, func
from loguru import logger
from typing import Union

import datetime


router = APIRouter()

COOKIE_SAMESITE = settings.COOKIE_SAMESITE
COOKIE_SECURE = settings.COOKIE_SECURE
COOKIE_DOMAIN = settings.COOKIE_DOMAIN

@router.post("/signup", dependencies=[Depends(RateLimiter(calls=10, period=60))])
async def signup(
    request: Request,
    response: Response,
    user_data: UserModel,
    session: Session = Depends(get_session),
) -> Union[dict, str]:
    try:
        hashed_host = encode_host(get_real_ip(request))
        count_hosts = session.exec(
            select(func.count())
            .select_from(Users)
            .where(Users.hash_host == hashed_host)
        ).one()

        if count_hosts >= 3:
            raise HTTPException(status_code=400, detail="TOO_MANY_USERS_PER_HOST")

        existing_user = session.exec(select(Users).where(Users.name == user_data.user)).first()

        if existing_user:
            raise HTTPException(status_code=400, detail="USERNAME_ALREADY_TAKEN ")

        new_user = Users(
            name=user_data.user,
            email=user_data.email,
            password=token_manager.encode(token=user_data.password),
            created_at=datetime.datetime.utcnow(),
            hash_host=hashed_host,
        )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        access_token = create_access_token(str(new_user.id), str(settings.SECRET_KEY))
        refresh_token = token_manager.encode(str(new_user.id))

        await redis_client.set(f"session:{access_token}", new_user.id, ex=60 * 15)
        await redis_client.set(
            f"refresh:{refresh_token}", new_user.id, ex=60 * 60 * 24 * 7
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

        access_token = create_access_token(str(new_user.id), str(settings.SECRET_KEY))
        refresh_token = token_manager.encode(str(new_user.id))

        await redis_client.set(f"session:{access_token}", new_user.id, ex=60 * 15)
        await redis_client.set(
            f"refresh:{refresh_token}", new_user.id, ex=60 * 60 * 24 * 7
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

        return {"message": "User created successfully"}

    except HTTPException:
        raise

    except Exception as err:
        logger.info(f"Error creating user: {err}")
        raise HTTPException(status_code=500, detail="Error creating user")
