# Quickstart Guide: Phase 1 and Phase 2 Applications

## Overview
This guide explains how to run both Phase 1 (console app) and Phase 2 (web app) after the structural separation.

## Prerequisites
- Python 3.11+
- Node.js 18+ (for frontend)
- uv package manager
- Access to Neon PostgreSQL database (for Phase 2)

## Phase 1 - Console Application

### Location
`phase-1-console/`

### Setup
```bash
cd phase-1-console
pip install -e .
# Or if using uv:
uv pip install -e .
```

### Usage
```bash
# Interactive mode
python -m src.todo.main

# CLI mode examples
python -m src.todo.main add "Buy groceries" "Milk, bread, eggs"
python -m src.todo.main list
python -m src.todo.main complete 1
python -m src.todo.main update 1 --title "Updated task title"
```

### Features
- Add, list, update, complete, delete tasks
- Export tasks to JSON
- Import tasks from JSON
- Interactive mode for easy use

## Phase 2 - Web Application

### Location
`phase-2-web/`

### Backend Setup
```bash
cd phase-2-web/backend
pip install -e .
# Or if using uv:
uv pip install -e .
```

### Backend Environment Variables
Create `.env` file in `phase-2-web/backend/`:
```env
DATABASE_URL=postgresql://username:password@neon-host/dbname
BETTER_AUTH_SECRET=your-jwt-secret-here
ENVIRONMENT=development
```

### Backend Usage
```bash
# Method 1: Using uvicorn directly
cd phase-2-web/backend
uv run uvicorn phase-2-web.backend.main:app --reload --port 8000

# Method 2: Using run_backend.py (after updating import paths)
python run_backend.py
```

### Frontend Setup
```bash
cd phase-2-web/frontend
npm install
```

### Frontend Usage
```bash
cd phase-2-web/frontend
npm run dev
```

### API Endpoints (Phase 2)
- `GET /` - Health check
- `GET /health` - Health check
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /api/tasks` - Get user's tasks
- `POST /api/tasks` - Create task
- `PUT /api/tasks/{task_id}` - Update task
- `DELETE /api/tasks/{task_id}` - Delete task
- `PATCH /api/tasks/{task_id}/toggle` - Toggle task completion

## Development Workflow

### Running Both Applications Together
1. Start backend: `uv run uvicorn phase-2-web.backend.main:app --reload --port 8000`
2. Start frontend: `cd phase-2-web/frontend && npm run dev`
3. Console app available separately: `python -m phase-1-console.src.todo.main`

### Testing
```bash
# Backend tests
cd phase-2-web/backend
python -m pytest

# Console app functionality
cd phase-1-console
python -c "from src.todo.main import main; main()"
```

## Deployment Preparation

### Hugging Face Deployment
The `pyproject.toml` remains at the repository root to maintain deployment compatibility. The backend structure allows deployment with the command:
```bash
uv run uvicorn phase-2-web.backend.main:app --host 0.0.0.0 --port 7860
```

### Database Migration
Phase 2 uses Neon PostgreSQL with automatic table creation on startup. The database schema is managed through SQLModel migrations.