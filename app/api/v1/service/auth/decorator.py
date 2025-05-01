from fastapi import Request, HTTPException, status
from dotenv import load_dotenv
from datetime import datetime
from functools import wraps

import os

load_dotenv(override=True)

AUTH_TOKEN = os.getenv('AUTHORIZATION_KEY')
BEARER_PREFIX = "Bearer " 

def AuthService(func):
    """
    Authentication decorator for FastAPI endpoints.
    
    Validates Bearer token in Authorization header against environment variable.
    
    Args:
        func: The FastAPI endpoint function to wrap
        
    Returns:
        Wrapped function with auth check
        
    Raises:
        HTTPException(401): If authentication fails
    """
    unauthorized_response = {
        "status": "error",
        "message": "You don't have permission to access this resource",
        "timestamp": None 
    }

    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
                
        try:
            if not auth_header:
                unauthorized_response["timestamp"] = datetime.now().isoformat()
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=unauthorized_response)

            scheme, token = auth_header.split(' ', 1)

            if scheme.lower() != 'bearer' or token != AUTH_TOKEN:
                unauthorized_response["timestamp"] = datetime.now().isoformat()
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=unauthorized_response)
            
            return await func(request, *args, **kwargs)
            
        except ValueError:
            unauthorized_response["timestamp"] = datetime.now().isoformat()
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=unauthorized_response)

    return wrapper