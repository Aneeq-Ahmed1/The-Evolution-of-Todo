# Todo Application - Phase 1 & Phase 2

A comprehensive todo application with both console and web interfaces. Phase 1 provides a command-line interface, while Phase 2 offers a web application with authentication and database persistence.

## Features

### Phase 1 - Console App
- Add, view, update, complete, and delete tasks
- Task expiration after 24 hours of inactivity
- Import/export tasks in JSON format
- Command-line interface

### Phase 2 - Web App
- User authentication with JWT
- Create, read, update, and delete tasks
- PostgreSQL database with Neon integration
- RESTful API endpoints
- Frontend interface (coming soon)

## Requirements

- Python 3.11+
- uv package manager
- Node.js 18+ (for frontend development)

## Project Structure

```
├── phase-1-console/          # Phase 1: Console application
│   └── src/todo/             # Console app source code
├── phase-2-web/              # Phase 2: Web application
│   ├── frontend/             # Frontend components
│   └── backend/              # Backend API with FastAPI
├── pyproject.toml            # Project dependencies (root level)
└── run_backend.py            # Script to start backend server
```

## Phase 1 - Console App Setup

1. Navigate to the console app: `cd phase-1-console`
2. Install dependencies: `uv sync`
3. Run the application: `uv run python -m src.todo.main [command] [arguments]`

### Console App Usage

```
python -m src.todo.main [command] [arguments]

Available commands:
  add          Add a new task
  list         List all tasks
  update       Update a task
  complete     Mark task as complete
  uncomplete   Mark task as pending
  delete       Delete a task
  export       Export tasks to JSON
  import       Import tasks from JSON file
```

#### Console App Examples

- Add a task: `uv run python -m src.todo.main add "Buy groceries" "Milk, bread, eggs"`
- List tasks: `uv run python -m src.todo.main list`
- Complete a task: `uv run python -m src.todo.main complete 1`
- Update a task: `uv run python -m src.todo.main update 1 --title "Buy groceries (done)" --description "Milk, bread, eggs, fruits"`
- Delete a task: `uv run python -m src.todo.main delete 1`

## Phase 2 - Web App Backend Setup

1. Install project dependencies: `uv sync`
2. Set up environment variables in `.env` file:
   ```
   DATABASE_URL=postgresql://username:password@neon-host/dbname
   BETTER_AUTH_SECRET=your-jwt-secret-here
   ```
3. Run the backend: `python run_backend.py` or `uv run uvicorn phase_2_web.backend.main:app --reload --port 8000`

### Web App API Endpoints

- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /api/tasks` - Get user's tasks
- `POST /api/tasks` - Create task
- `PUT /api/tasks/{task_id}` - Update task
- `DELETE /api/tasks/{task_id}` - Delete task
- `PATCH /api/tasks/{task_id}/toggle` - Toggle task completion
- `GET /health` - Health check

## Architecture

### Phase 1 Architecture
- **CLI Layer**: Handles user input/output via command-line arguments
- **Domain Layer**: Task entity and TaskManager for business logic
- **Data Storage**: In-memory dictionary with automatic cleanup of expired tasks

### Phase 2 Architecture
- **API Layer**: FastAPI with JWT authentication
- **Business Layer**: TaskService for business logic
- **Data Layer**: SQLModel with PostgreSQL database
- **Security Layer**: JWT-based authentication and authorization