from pydantic_settings import BaseSettings
from starlette.config import Config

import os


config = Config(os.environ.get("APP_ENV"))
    
class DatabaseSettings(BaseSettings):
    DB_URL: str = config("DB_URL")
    
class RedisSettings(BaseSettings):
    REDIS_HOST: str = config("REDIS_HOST")
    REDIS_PORT: int = config("REDIS_PORT")
    REDIS_PASSWORD: str = config("REDIS_PASSWORD")
    
class TokenManagerSettings(BaseSettings):
    SECRET_KEY: str = config("SECRET_KEY")
    
class APISettings(BaseSettings):
    API_MODE: str = config("API_MODE")
    AUTHORIZATION_KEY: str = config("AUTHORIZATION_KEY")
    COOKIE_SAMESITE: str = config("COOKIE_SAMESITE")
    COOKIE_SECURE: bool = config("COOKIE_SECURE")
    COOKIE_DOMAIN: str = config("COOKIE_DOMAIN")
    
    SENTRY_DSN: str = config("SENTRY_DSN")

class Settings(
    DatabaseSettings,
    RedisSettings,
    TokenManagerSettings,
    APISettings,
):
    pass
        

settings = Settings()