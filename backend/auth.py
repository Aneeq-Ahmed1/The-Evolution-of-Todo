from fastapi import HTTPException, Depends, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import jwt
from jwt.exceptions import PyJWTError, ExpiredSignatureError
from datetime import datetime, timezone
from .settings import settings
from .schemas import TokenData


# Initialize security scheme
security = HTTPBearer()


def verify_token(token: str) -> TokenData:
    """
    Verify JWT token and extract user information.
    """
    try:
        # Decode the token using the shared secret
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=["HS256"]  # Using HS256 as specified in the spec
        )

        # Extract user_id and email from the payload
        user_id: str = payload.get("id")
        email: str = payload.get("email")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials: Missing user_id"
            )

        token_data = TokenData(user_id=user_id, email=email)
        return token_data

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> TokenData:
    """
    Dependency to get current user from JWT token.
    """
    token_data = verify_token(credentials.credentials)
    return token_data


def verify_user_id_match(jwt_user_id: str, url_user_id: str) -> bool:
    """
    Verify that the user_id in the JWT matches the user_id in the URL.
    """
    if jwt_user_id != url_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID in token does not match user ID in URL"
        )
    return True