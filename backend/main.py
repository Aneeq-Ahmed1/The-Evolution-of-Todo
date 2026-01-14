import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

# Import using absolute imports for compatibility
from phase_2_web.backend.routes import tasks, auth
from phase_2_web.backend.settings import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


from sqlmodel import SQLModel
from phase_2_web.backend.db import engine
from phase_2_web.backend import models  # Import all models to register them

# Ensure all models are registered before creating tables
from phase_2_web.backend.models import User, Task  # Explicitly import models to ensure they're registered


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
            result = session.exec(text("SELECT current_database();"))
            current_db = result.first()
            if current_db:
                logger.info(f"Connected to database: {current_db}")

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
app.include_router(auth.router, tags=["auth"])


# Root endpoint for health check
@app.get("/")
def read_root():
    return {"message": "Todo API is running"}


# Debug endpoint to check database status
@app.get("/api/debug/db-status")
def debug_db_status():
    from sqlalchemy import text
    from phase_2_web.backend.db import engine
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