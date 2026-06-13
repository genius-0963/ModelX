"""
Authentication and Authorization.

Provides JWT token verification and API key fallback for secure endpoint access.
"""

import uuid
from typing import Annotated

from fastapi import Depends, HTTPException, Header, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from src.config.settings import get_settings

# In a real system, this would be validated against a database
# For this scaffold, we provide a mock user model
class User(BaseModel):
    id: uuid.UUID
    email: str
    is_active: bool = True

# OAuth2 scheme for swagger UI integration
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

async def get_current_user(
    token: Annotated[str | None, Depends(oauth2_scheme)],
    api_key: Annotated[str | None, Header(alias="X-API-Key")] = None,
) -> User:
    """
    Validate credentials and return the current user.
    Supports both JWT Bearer tokens and custom X-API-Key header.
    """
    settings = get_settings()
    
    # This is a mock implementation. 
    # In production, you would verify the JWT signature or lookup the API key in the DB.
    
    if not token and not api_key:
        # In development, return a mock user if auth is not strictly required
        if settings.environment == "development":
            return User(id=uuid.UUID("00000000-0000-0000-0000-000000000000"), email="dev@example.com")
            
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated. Provide Bearer token or X-API-Key header.",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # For now, just return a mock user if any token is provided
    # A complete implementation would decode the JWT and fetch user details
    return User(
        id=uuid.UUID("11111111-1111-1111-1111-111111111111"), 
        email="user@example.com"
    )
