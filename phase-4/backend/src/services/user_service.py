"""
User service for authentication operations.
"""
from sqlmodel import Session, select
from ..models.user import User, UserCreate
from ..utils.password import hash_password, verify_password


def create_user(session: Session, user: UserCreate) -> User:
    """
    Create a new user with hashed password.
    """
    hashed_password = hash_password(user.password)
    db_user = User(
        email=user.email,
        password_hash=hashed_password
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def authenticate_user(session: Session, email: str, password: str) -> User | None:
    """
    Authenticate user by email and password.
    """
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()

    if not user or not verify_password(password, user.password_hash):
        return None

    return user


def get_user_by_email(session: Session, email: str) -> User | None:
    """
    Get user by email.
    """
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()