from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
from ..database import get_session
from ..models.user import User
from ..schemas.auth import TokenData
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Get secret key from environment
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is not set")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"SECRET_KEY loaded: {'Yes' if SECRET_KEY else 'No'}")

ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

security = HTTPBearer()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a new access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    """
    Verify the access token.
    """
    try:
        logger.info(f"Attempting to decode token: {token[:20]}..." if token else "Token is None")
        logger.info(f"Using SECRET_KEY: {SECRET_KEY[:10]}..." if SECRET_KEY else "SECRET_KEY is None")
        logger.info(f"Using ALGORITHM: {ALGORITHM}")

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.info(f"Decoded payload: {payload}")

        email: str = payload.get("sub")
        if email is None:
            logger.error("No email found in token payload")
            raise credentials_exception
        token_data = TokenData(email=email)
        logger.info(f"Token verified successfully for email: {email}")
    except JWTError as e:
        logger.error(f"JWT Error during token verification: {str(e)}")
        raise credentials_exception
    except Exception as e:
        logger.error(f"Unexpected error during token verification: {str(e)}")
        raise credentials_exception
    return token_data


async def get_current_user_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Get the current user token from the authorization header.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    logger.info(f"Received token: {credentials.credentials[:20] if credentials.credentials else 'None'}...")
    token = credentials.credentials
    return token


async def get_current_user(token: str = Depends(get_current_user_token)):
    """
    Get the current user from the token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    logger.info(f"Verifying token in get_current_user: {token[:20] if token else 'None'}...")
    return verify_token(token, credentials_exception)