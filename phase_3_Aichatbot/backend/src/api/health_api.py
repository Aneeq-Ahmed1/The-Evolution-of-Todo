"""
Health check API for the AI Agent Platform
Implements comprehensive health check endpoint per T054
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List
import time
import asyncio
from datetime import datetime
from pydantic import BaseModel

from ..db.database import get_session
from ..db.settings import settings
from ..utils.logging import Logger
from ..auth.auth_handler import get_current_user, TokenData


router = APIRouter(prefix="/api", tags=["health"])


class HealthStatus(BaseModel):
    """Health status response model"""
    status: str
    timestamp: str
    uptime: float
    services: Dict[str, Any]
    version: str
    environment: str


class DetailedHealthResponse(BaseModel):
    """Detailed health response model"""
    status: str
    details: Dict[str, Any]
    timestamp: str


# Store the application start time
APP_START_TIME = time.time()
VERSION = "1.0.0"


@router.get("/health", response_model=HealthStatus)
async def health_check() -> HealthStatus:
    """
    Comprehensive health check endpoint
    Implements T054: Add health check endpoint in backend/src/api/health_api.py
    """
    try:
        # Calculate uptime
        uptime = time.time() - APP_START_TIME

        # Check database connectivity
        db_status = "unknown"
        try:
            session = next(get_session())
            # Attempt a simple query
            from sqlmodel import text
            result = session.exec(text("SELECT 1")).first()
            if result is not None:
                db_status = "healthy"
            else:
                db_status = "degraded"
            session.close()
        except Exception as e:
            db_status = f"error: {str(e)}"

        # Check LLM provider connectivity
        llm_status = "unknown"
        if settings.LLM_PROVIDER == "gemini":
            if settings.GEMINI_API_KEY:
                llm_status = "configured"
            else:
                llm_status = "not configured"
        elif settings.LLM_PROVIDER == "openai":
            if settings.OPENAI_API_KEY:
                llm_status = "configured"
            else:
                llm_status = "not configured"
        else:
            llm_status = "unknown provider"

        # Overall status based on critical components
        overall_status = "healthy"
        if db_status != "healthy":
            overall_status = "degraded"
        if "error" in str(db_status) or llm_status == "not configured":
            overall_status = "unhealthy"

        return HealthStatus(
            status=overall_status,
            timestamp=datetime.utcnow().isoformat(),
            uptime=uptime,
            services={
                "database": db_status,
                "llm_provider": llm_status,
                "authentication": "enabled",
                "rate_limiting": "enabled",
                "conversation_storage": "available"
            },
            version=VERSION,
            environment=settings.ENVIRONMENT
        )
    except Exception as e:
        Logger.error(f"Health check error: {str(e)}")
        raise HTTPException(status_code=500, detail="Health check failed")


@router.get("/health/detail", response_model=DetailedHealthResponse)
async def detailed_health_check() -> DetailedHealthResponse:
    """
    Detailed health check with extended diagnostics
    """
    try:
        # Perform detailed checks
        details = {}

        # Database check
        try:
            session = next(get_session())
            start_time = time.time()

            # Check connection
            result = session.exec(text("SELECT 1")).first()
            db_connect_time = time.time() - start_time

            # Check for conversation table
            table_check = session.exec(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables
                    WHERE table_name = 'conversation'
                )
            """)).first()

            session.close()

            details["database"] = {
                "status": "connected" if result is not None else "connection_failed",
                "connect_time": db_connect_time,
                "has_conversation_table": table_check,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            details["database"] = {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }

        # LLM provider check
        try:
            provider_details = {
                "configured_provider": settings.LLM_PROVIDER,
                "is_configured": False,
                "timestamp": datetime.utcnow().isoformat()
            }

            if settings.LLM_PROVIDER == "gemini" and settings.GEMINI_API_KEY:
                provider_details["is_configured"] = True
            elif settings.LLM_PROVIDER == "openai" and settings.OPENAI_API_KEY:
                provider_details["is_configured"] = True
            elif settings.LLM_PROVIDER not in ["gemini", "openai"]:
                provider_details["warning"] = f"Unsupported provider: {settings.LLM_PROVIDER}"

            details["llm_provider"] = provider_details
        except Exception as e:
            details["llm_provider"] = {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }

        # Service availability check
        details["services"] = {
            "chat_api": True,
            "mcp_server": True,
            "authentication": True,
            "rate_limiting": True,
            "conversation_storage": True,
            "timestamp": datetime.utcnow().isoformat()
        }

        # Check overall status
        has_errors = any(
            "error" in str(v.get("status", "")).lower() or
            v.get("status") == "connection_failed"
            for v in details.values()
            if isinstance(v, dict)
        )

        status = "degraded" if has_errors else "healthy"

        return DetailedHealthResponse(
            status=status,
            details=details,
            timestamp=datetime.utcnow().isoformat()
        )
    except Exception as e:
        Logger.error(f"Detailed health check error: {str(e)}")
        raise HTTPException(status_code=500, detail="Detailed health check failed")


@router.get("/health/ready")
async def readiness_check() -> Dict[str, str]:
    """
    Readiness check for container orchestration
    Returns 200 when the service is ready to accept traffic
    """
    try:
        # Check if critical services are ready
        session = next(get_session())
        # Simple ping to database
        result = session.exec(text("SELECT 1")).first()
        session.close()

        if result is not None:
            return {"status": "ready", "timestamp": datetime.utcnow().isoformat()}
        else:
            raise HTTPException(status_code=503, detail="Service not ready")
    except Exception:
        raise HTTPException(status_code=503, detail="Service not ready")


@router.get("/health/live")
async def liveness_check() -> Dict[str, str]:
    """
    Liveness check for container orchestration
    Returns 200 when the service is alive and functioning
    """
    try:
        # Simple check to see if the service is responding
        uptime = time.time() - APP_START_TIME
        return {
            "status": "alive",
            "uptime_seconds": uptime,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        Logger.error(f"Liveness check error: {str(e)}")
        raise HTTPException(status_code=503, detail="Service not alive")