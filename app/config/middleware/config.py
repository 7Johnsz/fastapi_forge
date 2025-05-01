from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi import Request, BackgroundTasks
from fastapi.responses import ORJSONResponse

# SlowAPI
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from slowapi import Limiter

# Services
from ...v1.service.webhook.config import webhook

# Utils
import redis.asyncio as redis
import os

redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")
redis_password = os.getenv("REDIS_PASSWORD")

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=f"redis://default:{redis_password}@{redis_host}:{redis_port}/1", 
    key_prefix="rate_limit:"
)

redis_pool = redis.ConnectionPool(
    host=redis_host, 
    password=redis_password,
    port=int(redis_port),
    db=1,
    decode_responses=True
)
redis_client = redis.Redis(connection_pool=redis_pool)

async def notify_rate_limit(request: Request, ip: str, limit_detail: str):
    """
    Sends a warning message to a Discord webhook when a rate limit is exceeded.

    This function is triggered when a user surpasses the allowed request rate.
    It sends details like the request path, method, IP address, user agent,
    and the specific rate limit details to a Discord webhook for monitoring
    and alerting purposes.

    Args:
        request (Request): The incoming FastAPI request object.
        ip (str): The IP address of the client that exceeded the rate limit.
        limit_detail (str): Details about the rate limit that was exceeded.
    """
    await webhook.warning_message(
        path=str(request.url.path),
        method=str(request.method),
        ip_adress=str(ip), 
        user_agent=request.headers.get("User-Agent"),
        description=(
            "⚠️ API Rate limit exceeded!\n"
            "A user has reached the request limit."
        ),
        content=(
            f"⏱️ Limit: {limit_detail}\n"
        )
    )

async def rate_limit_exception_handler(request: Request, exc: RateLimitExceeded):
    """
    Custom exception handler for RateLimitExceeded.

    This function is called when a RateLimitExceeded exception is raised.
    It will send a notification to the webhook channel only once per IP within
    a 60-second window, using Redis SETNX to ensure atomicity.

    :param request: The FastAPI request object.
    :param exc: The RateLimitExceeded exception object.
    """
    client_ip = get_remote_address(request)
    limit_detail = exc.detail
    
    notification_key = f"notified:{client_ip}"
    
    was_set = await redis_client.setnx(notification_key, "1")
    
    if was_set:
        ttl = 60
        await redis_client.expire(notification_key, ttl)
        
        background_tasks = BackgroundTasks()
        background_tasks.add_task(notify_rate_limit, request, client_ip, limit_detail)
        await background_tasks()
    
    return ORJSONResponse(
        status_code=429,
        content={"message": "Too many requests. Please try again later."}
    )

def configure_middleware(app):
    """
    Configure the FastAPI application with various middlewares.

    This function sets up the application with the following middlewares:

    - SlowAPIMiddleware: A middleware to handle rate limiting.
    - GZipMiddleware: A middleware to compress responses larger than 1000 bytes.
    - CORSMiddleware: A middleware to enable CORS on the application.

    :param app: The FastAPI application instance.
    """
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, rate_limit_exception_handler)
    app.add_middleware(SlowAPIMiddleware)
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["localhost", "127.0.0.1"], 
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    
    # Uncomment the following lines to restrict access to specific hosts

    # @app.middleware("http")
    # async def restrict_requests(request: Request, call_next):
    #     print(request.client.host)
        
    #     allowed_hosts = ["localhost", "172.20.0.1", "127.0.0.1", "144.22.217.14", "172.19.0.1"]

    #     if request.client.host not in allowed_hosts:
    #         return ORJSONResponse(
    #             status_code=403,
    #             content={"message": "You don't have permission to access this resource"}
    #         )
        
    #     response = await call_next(request)
    #     return response