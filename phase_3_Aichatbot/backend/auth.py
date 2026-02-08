from fastapi import HTTPException, Depends, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import jwt
from jwt.exceptions import PyJWTError, ExpiredSignatureError
from datetime import datetime, timezone
from settings import settings
from schemas import TokenData


# Initialize security scheme
security = HTTPBearer()


def verify_token(token: str) -> TokenData:
    """
    Verify JWT token and extract user information.
    """
    try:
        print(f"DEBUG: Attempting to verify token: {token[:30]}...")  # Debug logging
        print(f"DEBUG: Using secret: {settings.BETTER_AUTH_SECRET[:10]}...")  # Debug logging
        print(f"DEBUG: Secret length: {len(settings.BETTER_AUTH_SECRET)}")  # Debug logging
        
        # Decode the token using the shared secret
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=["HS256"]  # Using HS256 as specified in the spec
        )

        print(f"DEBUG: Token payload: {payload}")  # Debug logging
        # Extract user_id and email from the payload
        user_id: str = payload.get("id")
        email: str = payload.get("email")

        if user_id is None:
            print("DEBUG: Missing user_id in token payload")  # Debug logging
            print(f"DEBUG: Available keys in payload: {list(payload.keys())}")  # Debug logging
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials: Missing user_id"
            )

        token_data = TokenData(user_id=user_id, email=email)
        print(f"DEBUG: Successfully verified token for user: {user_id}")  # Debug logging
        return token_data

    except jwt.ExpiredSignatureError:
        print("DEBUG: Token has expired")  # Debug logging
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidSignatureError:
        print("DEBUG: Invalid token signature - possible secret mismatch")  # Debug logging
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials: Invalid token signature"
        )
    except jwt.DecodeError as e:
        print(f"DEBUG: JWT Decode Error: {str(e)}")  # Debug logging
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials: Invalid token format"
        )
    except PyJWTError as e:
        print(f"DEBUG: JWT Error: {str(e)}")  # Debug logging
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )


def get_current_user(
    request: Request,  # Add request parameter to access headers
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> TokenData:
    """
    Dependency to get current user from JWT token.
    """
    # Log the incoming request headers for debugging
    print(f"DEBUG: Request headers: {dict(request.headers)}")
    print(f"DEBUG: Authorization header: {credentials.credentials[:20] if credentials.credentials else 'None'}...")
    
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