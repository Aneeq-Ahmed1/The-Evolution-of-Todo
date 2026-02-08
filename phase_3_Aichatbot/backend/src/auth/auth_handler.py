"""
Authentication Handler for the AI Agent Platform
Implements user authentication with session management per FR-013
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from uuid import UUID
import os
from ..db.settings import settings
from ..utils.logging import Logger


security = HTTPBearer()


class TokenData(BaseModel):
    """Token data model - matches the schema from schemas.py"""
    user_id: str
    email: Optional[str] = None
    name: Optional[str] = None


class AuthHandler:
    """Authentication handler class implementing JWT-based authentication"""

    def __init__(self):
        self.secret = settings.secret_key
        self.algorithm = "HS256"
        self.access_token_expire_minutes = settings.access_token_expire_minutes

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Create an access token with the given data

        Args:
            data: Dictionary containing user information
            expires_delta: Optional timedelta for token expiration

        Returns:
            Encoded JWT token string
        """
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)

        to_encode.update({"exp": expire.timestamp()})

        encoded_jwt = jwt.encode(to_encode, self.secret, algorithm=self.algorithm)
        return encoded_jwt

    def decode_access_token(self, token: str) -> Optional[TokenData]:
        """
        Decode and validate an access token

        Args:
            token: JWT token string

        Returns:
            TokenData object if valid, None if invalid
        """
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])

            # The login endpoint creates tokens with "id" field, not "user_id"
            user_id: str = payload.get("id") or payload.get("user_id")
            email: str = payload.get("email")
            name: str = payload.get("name") or payload.get("username")

            if user_id is None:
                return None

            token_data = TokenData(
                user_id=user_id,
                email=email,
                name=name
            )

            return token_data
        except jwt.JWTError as e:
            Logger.error(f"JWT Error: {str(e)}")
            return None

    async def get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
        """
        Get the current authenticated user from the token

        Args:
            credentials: HTTP Authorization credentials

        Returns:
            TokenData object for the authenticated user

        Raises:
            HTTPException: If authentication fails
        """
        token = credentials.credentials

        token_data = self.decode_access_token(token)
        if token_data is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return token_data

    def create_mock_user_token(self, user_id: str, username: str = "mock_user") -> str:
        """
        Create a mock user token for testing purposes

        Args:
            user_id: Unique user identifier
            username: Username for the user

        Returns:
            JWT token string
        """
        data = {
            "user_id": user_id,
            "username": username
        }

        return self.create_access_token(data)


# Create a global instance of the auth handler
auth_handler = AuthHandler()


# Dependency to get current user
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
    """
    Dependency to get the current authenticated user

    Args:
        credentials: HTTP Authorization credentials

    Returns:
        TokenData object for the authenticated user
    """
    return await auth_handler.get_current_user(credentials)


# Helper function to validate user access to resources
def validate_user_access(user_id: str, resource_user_id: str) -> bool:
    """
    Validate if a user has access to a resource based on user ID

    Args:
        user_id: The authenticated user's ID
        resource_user_id: The resource owner's ID

    Returns:
        Boolean indicating if access is allowed
    """
    # Convert both to UUID for comparison if possible
    try:
        user_uuid = UUID(user_id) if isinstance(user_id, str) else user_id
        resource_uuid = UUID(resource_user_id) if isinstance(resource_user_id, str) else resource_user_id
        return user_uuid == resource_uuid
    except ValueError:
        # If not valid UUIDs, compare as strings
        return str(user_id) == str(resource_user_id)


# Helper function to validate user ownership
def validate_user_ownership(current_user: TokenData, resource_user_id: str) -> bool:
    """
    Validate if the current user owns a resource

    Args:
        current_user: TokenData for the authenticated user
        resource_user_id: The resource owner's ID

    Returns:
        Boolean indicating if the user owns the resource
    """
    return validate_user_access(current_user.user_id, resource_user_id)


# Middleware-style function for checking authentication
async def require_authentication(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
    """
    Require authentication for an endpoint

    Args:
        credentials: HTTP Authorization credentials

    Returns:
        TokenData object for the authenticated user
    """
    return await auth_handler.get_current_user(credentials)