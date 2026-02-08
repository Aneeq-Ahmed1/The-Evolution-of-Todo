"""
Main FastAPI application entry point for the AI Chatbot.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.chat import router as chat_router
from .api.tasks import router as tasks_router
from .api.mapping import router as mapping_router
from .api.auth import router as auth_router
from .api.admin import router as admin_router
from .database import engine
from .models.chat_task import ChatTask
from .models.conversation import Conversation
from .models.message import Message
from .models.task import Task
from .models.user import User

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create database tables
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(bind=engine)
    yield
    # Shutdown: Add any cleanup here if needed


# Create the FastAPI app
app = FastAPI(
    title="Todo AI Chatbot API",
    description="API for AI-powered Todo chatbot with natural language processing",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js development server
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "http://localhost:3002",
        "http://127.0.0.1:3002",
        "http://localhost:3003",
        "http://127.0.0.1:3003",
        "http://localhost:3004",
        "http://127.0.0.1:3004",
        "http://localhost:3005",
        "http://127.0.0.1:3005",
        "http://localhost:3006",  # Current frontend port
        "http://127.0.0.1:3006",
        "http://localhost:3007",
        "http://127.0.0.1:3007",
        "http://localhost:3008",
        "http://127.0.0.1:3008",
        "http://localhost:3009",  # Current frontend port
        "http://127.0.0.1:3009",
        "http://localhost:8080",  # Alternative port
        "http://127.0.0.1:8080",
        "http://localhost:8000",  # Allow self-requests during development
        "http://127.0.0.1:8000",
        "http://0.0.0.0:3000"    # Additional possible origin
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(chat_router)
app.include_router(tasks_router)
app.include_router(mapping_router)
app.include_router(auth_router)
app.include_router(admin_router)

@app.get("/")
def read_root():
    return {"message": "Todo AI Chatbot API is running!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)