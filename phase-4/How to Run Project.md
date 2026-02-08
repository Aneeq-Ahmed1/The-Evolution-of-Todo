# How to Run the Todo Evolution Project

This document provides step-by-step instructions for setting up and running the Todo Evolution full-stack application.

## Prerequisites

- Python 3.13 or higher
- Node.js 18+ for frontend
- UV package manager (recommended) or pip
- npm or yarn for frontend dependencies

## Project Structure

The project is organized as a full-stack monorepo with:
- `src/todo_app/` - Original CLI todo application
- `backend/` - FastAPI backend with authentication and database
- `frontend/` - Next.js frontend application
- `specs/` - Specification files for the project

## Setting Up the Backend (API Server)

### Using UV (Recommended)

1. **Install UV** (if not already installed):
   ```bash
   pip install uv
   ```

2. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

3. **Install dependencies**:
   ```bash
   uv venv
   uv pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Copy the `.env.example` file to `.env` and update the values:
   ```bash
   cp ../.env.example .env
   # Edit .env with your preferred editor
   ```

5. **Run the backend server**:
   ```bash
   cd src
   uv run uvicorn main:app --reload --port 8000
   ```

### Using Pip

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Copy the `.env.example` file to `.env` and update the values:
   ```bash
   cp ../.env.example .env
   # Edit .env with your preferred editor
   ```

5. **Run the backend server**:
   ```bash
   cd src
   uvicorn main:app --reload --port 8000
   ```

### Important: Backend Must Be Running

**The frontend will not work without the backend API running on port 8000.** Make sure the backend is running before starting the frontend.

## Setting Up the Frontend (UI)

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Set up environment variables**:
   Copy the `.env.example` file to `.env.local` and update the values:
   ```bash
   cp ../.env.example .env.local
   # Edit .env.local with your preferred editor
   ```

4. **Run the development server**:
   ```bash
   npm run dev
   ```

5. **Open your browser** to `http://localhost:3000`

## Running the Original CLI Application

The original CLI application can still be run from the project root:

1. **Using UV**:
   ```bash
   uv run python -m src.todo_app
   ```

2. **Using Pip**:
   ```bash
   python -m src.todo_app
   ```

## Running Tests

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm run test
```

### CLI Application Tests
```bash
python -m pytest tests/
```

## API Endpoints

Once the backend is running, you can access:
- API documentation: `http://localhost:8000/docs`
- API specification: `http://localhost:8000/openapi.json`
- Health check: `http://localhost:8000/`

## Troubleshooting

### Common Issues

1. **Port already in use**: If you get port conflicts, change the port numbers in the commands above.

2. **Dependency conflicts**: Make sure you're using Python 3.13+ and the latest versions of package managers.

3. **Environment variables missing**: Ensure all required environment variables are set in your `.env` files.

### Development Mode

For development, you can run both the backend and frontend simultaneously:
1. Open one terminal and run the backend server
2. Open another terminal and run the frontend development server
3. The frontend will proxy API requests to the backend server

## Database

The application uses SQLite by default, with the database file `todo.db` located in the project root and backend directory. The database will be created automatically when you first run the application.