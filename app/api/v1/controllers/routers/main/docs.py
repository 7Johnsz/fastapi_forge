from scalar_fastapi import get_scalar_api_reference
from fastapi.exceptions import HTTPException
from fastapi import Request, APIRouter

from ....controllers.config.settings import settings


router = APIRouter()

@router.get("/scalar", include_in_schema=False)
async def scalar_html(request: Request):
    if settings.API_MODE == "development":
        return get_scalar_api_reference(
            openapi_url=request.app.openapi_url, title=request.app.title
        )

    raise HTTPException(status_code=404, detail="Not Found")
