from scalar_fastapi import get_scalar_api_reference
from fastapi import Request

# Config
from ....service.auth.decorator import AuthService
from ......config.middleware.config import limiter
from ...config.api import router

@router.get("/scalar", include_in_schema=False)
@limiter.limit("30/minute")
@AuthService
async def scalar_html(request: Request):
    return get_scalar_api_reference(
        openapi_url=request.app.openapi_url,
        title=request.app.title)