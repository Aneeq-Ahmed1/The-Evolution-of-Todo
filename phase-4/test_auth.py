#!/usr/bin/env python3
"""
Debug script to test authentication functionality
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from sqlmodel import create_engine, Session
from sqlalchemy import text
import traceback
from backend.src.models.user import User, UserCreate
from backend.src.services.user_service import create_user
from backend.src.utils.password import hash_password
from backend.src.database import engine

def test_database_connection():
    """Test database connection"""
    try:
        print("Testing database connection...")
        with Session(engine) as session:
            result = session.exec(text("SELECT 1")).first()
            print(f"Database connection successful: {result}")
            return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        traceback.print_exc()
        return False

def test_user_creation():
    """Test user creation directly"""
    try:
        print("\nTesting user creation...")
        with Session(engine) as session:

            # Clean up any existing test user
            from sqlmodel import select
            existing_user = session.exec(select(User).where(User.email == "test@example.com")).first()
            if existing_user:
                session.delete(existing_user)
                session.commit()
                print("Cleaned up existing test user")

            # Create a new user
            user_data = UserCreate(email="test@example.com", password="TestPass123!")
            db_user = create_user(session, user_data)
            print(f"User created successfully: {db_user.email}")
            print(f"User ID: {db_user.id}")
            print(f"Hashed password length: {len(db_user.password_hash)}")

            return True
    except Exception as e:
        print(f"User creation failed: {e}")
        traceback.print_exc()
        return False

def test_password_hashing():
    """Test password hashing"""
    try:
        print("\nTesting password hashing...")
        password = "TestPass123!"
        hashed = hash_password(password)
        print(f"Password: {password}")
        print(f"Hashed: {hashed[:20]}...")
        print(f"Hash length: {len(hashed)}")

        # Test verification utility
        from src.utils.password import verify_password
        is_valid = verify_password(password, hashed)
        print(f"Verification result: {is_valid}")

        return True
    except Exception as e:
        print(f"Password hashing failed: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Starting authentication debugging...")

    success = True
    success &= test_database_connection()
    success &= test_password_hashing()
    success &= test_user_creation()

    if success:
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)