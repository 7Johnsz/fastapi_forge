from fastapi import Cookie, HTTPException
from .....config.middleware.redis import redis_client
from loguru import logger


async def AccessToken(access_token: str = Cookie(None)) -> int:
    """Dependency that validates access token and returns user_id"""
    
    if not access_token:
        logger.warning("No access_token cookie provided")
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        logger.debug(f"Looking for session key: session:{access_token[:20]}...")
        
        user_id_raw = await redis_client.get(f"session:{access_token}")
        
        if not user_id_raw:
            logger.warning(f"Session not found in Redis for token: {access_token[:20]}...")
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        
        logger.debug(f"Found user_id_raw: {user_id_raw} (type: {type(user_id_raw)})")
        
        user_id = int(user_id_raw)
        
        logger.info(f"AccessToken validated for user_id: {user_id}")
        
        return user_id
        
    except ValueError as e:
        logger.error(f"Error converting user_id: {e}")
        raise HTTPException(status_code=401, detail="INVALID_ACCESS_TOKEN")
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"Error validating access token: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")