# Research: Phase 1 and Phase 2 Separation

## Overview
This research document analyzes the current codebase structure to plan the separation of Phase 1 (console app) and Phase 2 (web app) into isolated directories.

## Current Structure Analysis

### Phase 1 - Console App (src/todo/)
- Located in `src/todo/` directory
- Main entry point: `src/todo/main.py` - handles both CLI and interactive modes
- Supporting files:
  - `src/todo/models.py` - Task model definition
  - `src/todo/manager.py` - Task management logic
  - `src/todo/interactive.py` - Interactive mode interface
  - `src/todo/__init__.py` - Package initialization

### Phase 2 - Web App Backend (backend/)
- Located in `backend/` directory
- Main entry point: `backend/main.py` - FastAPI application
- Key components:
  - `backend/auth.py` - JWT authentication
  - `backend/db.py` - Database connection with Neon PostgreSQL
  - `backend/models.py` - SQLModel definitions
  - `backend/routes/tasks.py` - Task API endpoints
  - `backend/routes/auth.py` - Authentication endpoints
  - `backend/schemas.py` - Pydantic models
  - `backend/settings.py` - Configuration management

### Frontend (frontend/)
- Located in `frontend/` directory
- Next.js application with:
  - App router in `frontend/app/`
  - Components in `frontend/components/`
  - Services in `frontend/services/`
  - Styles in `frontend/styles/`

### Shared Configuration
- `pyproject.toml` - Project dependencies and configuration (at root)
- `run_backend.py` - Script to run backend (imports from backend.main)
- Various test files scattered across the project

## Key Findings

### Import Patterns
- Backend uses imports like `from backend.routes import tasks, auth`
- Backend imports from `backend.models`, `backend.db`, etc.
- `run_backend.py` imports from `backend.main`

### Migration Requirements
1. Phase 1 files (src/todo/) → phase-1-console/src/todo/
2. Backend files (backend/) → phase-2-web/backend/
3. Frontend files (frontend/) → phase-2-web/frontend/
4. pyproject.toml must remain at root level
5. Import paths in backend may need updating after relocation

### Potential Issues
1. Import paths in backend after directory changes
2. `run_backend.py` will need to be updated to import from new location
3. Backend startup command needs to be adjusted to reflect new structure
4. Environment variables and configuration paths may need updates

## Decision: Maintain Backend Structure
**Rationale**: The backend currently has the correct structure with `backend/` prefix in imports. Moving it to `phase-2-web/backend/` should maintain functionality as long as imports are updated appropriately.

## Decision: Console App Isolation
**Rationale**: The console app in `src/todo/` will be moved to `phase-1-console/src/todo/` to isolate it from the web app components.

## Alternatives Considered
1. Keep src/ directory in root - Rejected because it doesn't achieve proper isolation between phases
2. Merge console and web app in same phase directory - Rejected because it goes against the requirement for separation
3. Convert console app to separate package - Rejected as it adds unnecessary complexity for this refactor

## Action Items for Implementation
1. Create phase-1-console/ directory and move src/ there
2. Create phase-2-web/ directory with frontend/ and backend/ subdirectories
3. Update import paths in backend to reflect new structure
4. Update run_backend.py to import from new location
5. Test backend functionality after changes
6. Update documentation to reflect new structure