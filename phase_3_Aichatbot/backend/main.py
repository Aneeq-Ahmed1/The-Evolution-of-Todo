import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

# Import using absolute imports for compatibility
from routes import tasks, auth
from settings import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


from sqlmodel import SQLModel
from db import engine
import models  # Import all main models to register them

# Import all models from src to ensure they're registered with SQLModel
from src.models import conversation, message, skill_log, agent_session

# Ensure all models are registered before creating tables
from models import User, Task  # Explicitly import models to ensure they're registered


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events.
    """
    # Startup
    logger.info("Application starting up...")

    # Log database URL for debugging (with credentials redacted)
    db_url = settings.DATABASE_URL
    safe_db_url = db_url
    if '@' in db_url:
        try:
            protocol_host_part = db_url.split('@')[0]
            host_db_part = db_url.split('@')[1]
            if '//' in protocol_host_part:
                safe_protocol = protocol_host_part.split('//')[0] + '//'
                safe_db_url = f"{safe_protocol}[REDACTED]@[{host_db_part}]"
            else:
                safe_db_url = f"[REDACTED]@[{host_db_part}]"
        except:
            safe_db_url = "[REDACTED]"

    logger.info(f"DATABASE_URL: {safe_db_url}")
    logger.info(f"Database type: PostgreSQL (Neon)")

    try:
        # Verify that models are registered by checking the metadata
        logger.info(f"Registered tables: {list(SQLModel.metadata.tables.keys())}")

        # Create database tables on startup (guaranteed execution)
        # Temporarily skip for PostgreSQL Neon to avoid schema conflicts
        if settings.DATABASE_URL.startswith("postgresql"):
            logger.info("Skipping automatic table creation for PostgreSQL (due to schema conflicts)...")
        else:
            logger.info("Creating database tables (if they don't exist)...")
            SQLModel.metadata.create_all(engine)
            logger.info("Database tables creation completed successfully!")

        # Additional verification: try to connect and check if tables exist
        from sqlmodel import Session
        from sqlalchemy import inspect
        with Session(engine) as session:
            inspector = inspect(engine)
            existing_tables = inspector.get_table_names()
            logger.info(f"Tables found in database: {existing_tables}")

            # Check specifically for our tables
            for table in ['user', 'task']:
                if table in existing_tables:
                    logger.info(f"Table '{table}' exists in database")
                else:
                    logger.warning(f"Table '{table}' does not exist in database")

            # Get database connection info for debugging
            from sqlalchemy import text
            try:
                result = session.exec(text("SELECT current_database();"))
                current_db = result.first()
                if current_db:
                    logger.info(f"Connected to database: {current_db}")
            except:
                logger.info("Could not retrieve database name (likely SQLite)")

            try:
                result = session.exec(text("SELECT current_setting('neon.branch_name', true);"))
                branch_name = result.first()
                if branch_name:
                    logger.info(f"Connected to Neon branch: {branch_name}")
                else:
                    logger.info("Not running on Neon (branch info not available)")
            except:
                logger.info("Could not retrieve Neon branch info")

            logger.info("Database connection and table verification completed successfully!")

        # Log API key configuration for debugging
        logger.info(f"GEMINI_API_KEY loaded: {'Yes' if settings.GEMINI_API_KEY else 'No'} (length: {len(settings.GEMINI_API_KEY) if settings.GEMINI_API_KEY else 0})")
        logger.info(f"OPENAI_API_KEY loaded: {'Yes' if settings.OPENAI_API_KEY else 'No'} (length: {len(settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else 0})")
        logger.info(f"LLM_PROVIDER selected: {settings.LLM_PROVIDER}")

        # Validate configuration on startup (temporarily disabled due to dependency conflicts)
        # try:
        #     from src.services.provider_service import provider_service
        #
        #     # Check if required configuration is present
        #     if not settings.gemini_api_key and not settings.openai_api_key:
        #         logger.error("No LLM provider API key found! Please set either GEMINI_API_KEY or OPENAI_API_KEY in environment variables.")
        #         raise ValueError("At least one LLM provider API key must be configured")
        #
        #     # Validate provider service configuration
        #     provider_info = provider_service.get_provider_info()
        #     logger.info(f"Available providers: {provider_info['available_providers']}")
        #     logger.info(f"Active provider: {provider_info['active_provider']}")
        #
        #     if not provider_info['available_providers']:
        #         logger.error("No valid LLM providers available! Check your API keys and configuration.")
        #         raise ValueError("No valid LLM providers available")
        #
        # except Exception as e:
        #     logger.error(f"Configuration validation failed: {str(e)}")
        #     raise

        # Run initial cleanup of expired conversations on startup
        # Commenting out due to schema mismatch in existing database
        # try:
        #     from src.services.conversation_service import ConversationService
        #     import asyncio
        #
        #     with Session(engine) as session:
        #         conversation_service = ConversationService(session)
        #         # Run the async method in an event loop
        #         deleted_count = asyncio.run(conversation_service.cleanup_expired_conversations())
        #         logger.info(f"Cleaned up {deleted_count} expired conversations on startup")
        # except Exception as e:
        #     logger.error(f"Error during initial conversation cleanup: {str(e)}")
        #     logger.info("Continuing startup despite conversation cleanup error")

    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise

    # Shutdown
    yield

    logger.info("Application shutting down...")


# Create FastAPI app instance
app = FastAPI(
    title="Todo API",
    description="FastAPI backend for Todo application with JWT authentication",
    version="0.1.0",
    lifespan=lifespan
)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routes
app.include_router(tasks.router, prefix="/api", tags=["tasks"])
app.include_router(auth.router, prefix="/api", tags=["auth"])

# Include the new user-specific chat route
try:
    from routes.chat import router as chat_router
    app.include_router(chat_router, prefix="/api", tags=["chat"])
except ImportError as e:
    logger.error(f"Failed to import user-specific chat router: {e}")
    import traceback
    logger.error(f"Full traceback: {traceback.format_exc()}")

# Include AI Agent Platform routes
try:
    import sys
    import os
    # Add the backend directory to the path to ensure proper imports
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    if backend_dir not in sys.path:
        sys.path.insert(0, backend_dir)
    
    from src.api.chat_api import router as chat_router
    app.include_router(chat_router)
except ImportError as e:
    logger.error(f"Failed to import chat router: {e}")
    import traceback
    logger.error(f"Full traceback: {traceback.format_exc()}")

try:
    from src.api.mcp_server import router as mcp_router
    app.include_router(mcp_router)
except ImportError as e:
    logger.error(f"Failed to import MCP router: {e}")

try:
    from src.api.health_api import router as health_router
    app.include_router(health_router)
except ImportError as e:
    logger.error(f"Failed to import health router: {e}")


# Root endpoint for health check
@app.get("/")
def read_root():
    return {"message": "Todo API is running"}


# Debug endpoint to check database status
@app.get("/api/debug/db-status")
def debug_db_status():
    from sqlalchemy import text
    from db import engine
    try:
        with engine.connect() as conn:
            # Get current database name
            result = conn.execute(text("SELECT current_database();"))
            current_db = result.scalar()

            # Get current schema
            result = conn.execute(text("SELECT current_schema();"))
            current_schema_name = result.scalar()

            # Get list of tables in public schema
            result = conn.execute(text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
            """))
            tables = [row[0] for row in result.fetchall()]

            # Get Neon branch info if available
            try:
                result = conn.execute(text("SELECT current_setting('neon.branch_name', true);"))
                branch_name = result.scalar()
            except:
                branch_name = None

            # Safe logging of DATABASE_URL with credentials redacted
            safe_db_url = settings.DATABASE_URL
            if '@' in settings.DATABASE_URL:
                try:
                    protocol_host_part = settings.DATABASE_URL.split('@')[0]
                    host_db_part = settings.DATABASE_URL.split('@')[1]
                    if '//' in protocol_host_part:
                        safe_protocol = protocol_host_part.split('//')[0] + '//'
                        safe_db_url = f"{safe_protocol}[REDACTED]@[{host_db_part}]"
                    else:
                        safe_db_url = f"[REDACTED]@[{host_db_part}]"
                except:
                    safe_db_url = "[REDACTED]"

            return {
                "connected_database_name": current_db,
                "connected_schema": current_schema_name,
                "list_of_tables": tables,
                "DATABASE_URL": safe_db_url,
                "neon_branch": branch_name,
                "environment": settings.ENVIRONMENT
            }
    except Exception as e:
        return {"error": str(e)}


# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "environment": settings.ENVIRONMENT}


# Global error handler for consistent error format
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


# Global error handler for validation errors
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


# Add validation error handler for request validation
from pydantic import ValidationError
from fastapi.exceptions import RequestValidationError

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": "Validation error", "errors": exc.errors()}
    )