"""
API Key authentication middleware
Validates x-api-key header for all incoming requests
"""
from fastapi import Header, HTTPException, status
from config import settings


async def verify_api_key(x_api_key: str = Header(...)):
    """
    Dependency to verify API key from request headers
    Raises 401 if key is invalid or missing
    """
    if x_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key"
        )
    return x_api_key
