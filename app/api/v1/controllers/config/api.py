from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="access_token")

router = APIRouter()