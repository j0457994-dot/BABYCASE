from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from .config import settings
import secrets

security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Simple API Key storage (in production, use database)
API_KEYS = {
    "admin": {
        "key": secrets.token_urlsafe(32),
        "role": "admin",
        "created_at": datetime.utcnow()
    }
}

def generate_api_key(user_id: str) -> str:
    """Generate a new API key for a user"""
    api_key = secrets.token_urlsafe(32)
    API_KEYS[user_id] = {
        "key": api_key,
        "role": "user",
        "created_at": datetime.utcnow()
    }
    return api_key

def verify_api_key(api_key: str) -> dict:
    """Verify an API key exists"""
    for user_id, data in API_KEYS.items():
        if data["key"] == api_key:
            return {"user_id": user_id, "role": data["role"]}
    return None

async def require_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Dependency for protecting endpoints"""
    api_key = credentials.credentials
    user = verify_api_key(api_key)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

def hash_password(password: str) -> str:
    """Hash a password for storage"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)