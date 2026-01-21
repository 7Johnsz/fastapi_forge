from ...controllers.config.settings import settings
from fastapi import Request, HTTPException, status

AUTH_TOKEN = settings.AUTHORIZATION_KEY

async def AuthService(request: Request):
    auth_header = request.headers.get('Authorization', '')
    if not auth_header:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED")
    
    try:
        scheme, token = auth_header.split(' ', 1)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED")
    
    if scheme.lower() != 'bearer' or token != AUTH_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED")