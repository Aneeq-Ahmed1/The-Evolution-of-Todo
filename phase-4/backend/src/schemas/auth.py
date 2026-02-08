from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class UserLogin(BaseModel):
    email: str
    password: str


class AdminLogin(BaseModel):
    """Admin login credentials."""
    email: str
    password: str


class PasswordReset(BaseModel):
    """Password reset request."""
    new_password: str