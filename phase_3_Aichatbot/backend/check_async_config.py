#!/usr/bin/env python3
"""
Script to check for async database configuration issues
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from sqlmodel import Session
from backend.src.db.database import engine

print("Checking database configuration...")

# Check if the engine is synchronous (which it appears to be based on the code)
print(f"Engine type: {type(engine)}")
print(f"Engine URL: {engine.url}")

# The issue is that the ConversationService expects an async session but gets a sync one
print("\nThe problem:")
print("- ConversationService methods are defined as 'async def'")
print("- But they receive a synchronous Session object from sqlmodel")
print("- This causes SQLAlchemy operational errors when async methods try to use sync sessions")
print("- The session.commit(), session.refresh(), etc. are synchronous operations")

print("\nSolutions needed:")
print("1. Either convert to fully async with AsyncEngine and AsyncSession")
print("2. Or convert methods to be synchronous (remove 'async' keyword)")

# Show what the async engine would look like
print("\nFor async operations, you would need:")
print("from sqlmodel.ext.asyncio.session import AsyncSession")
print("from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession")
print("# And use async operations like:")
print("# await session.commit()")
print("# await session.refresh(obj)")
print("# result = await session.exec(stmt)")