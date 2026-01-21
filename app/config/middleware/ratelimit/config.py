from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import ORJSONResponse
from ..redis import redis_client

def real_ip(request):
    ip = request.headers.get("CF-Connecting-IP")
    if ip:
        return ip

    xff = request.headers.get("X-Forwarded-For")
    if xff:
        return xff.split(",")[0].strip()
    return request.client.host

class RateLimiter(BaseHTTPMiddleware):
    def __init__(self, app, rules=None, calls=10, period=120):
        super().__init__(app)
        self.calls = calls
        self.period = period
        self.rules = rules if rules is not None else []

    async def dispatch(self, request, call_next):
        for path in self.rules:
            if request.url.path == path:
                
                client_ip = real_ip(request)
                
                key = f"rate_limit:{path}:{client_ip}"
                current = await redis_client.get(key)

                if current is None:
                    await redis_client.setex(key, self.period, 1)
                elif int(current) >= self.calls:
                    return ORJSONResponse(
                        status_code=429,
                        content={"message": "Too many requests. Please try again later."}
                    )
                else:
                    await redis_client.incr(key)
                break  

        return await call_next(request)