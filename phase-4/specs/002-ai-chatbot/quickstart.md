# Quickstart Guide: Todo AI Chatbot – Phase III (Basic Level)

## Prerequisites
- Python 3.9+ installed
- Node.js 18+ installed
- PostgreSQL database (Neon recommended)
- OpenAI API key
- Better Auth account

## Environment Setup

### Backend Environment
```bash
# Create backend/.env file
DATABASE_URL="postgresql://user:pass@host:port/database"
OPENAI_API_KEY="sk-..."
BETTER_AUTH_URL="..."
BETTER_AUTH_SECRET="..."
NEXT_PUBLIC_API_BASE_URL="http://localhost:8000"
```

### Frontend Environment
```bash
# Create frontend/.env.local file
NEXT_PUBLIC_API_BASE_URL="http://localhost:8000"
NEXT_PUBLIC_BASE_URL="http://localhost:3000"
```

## Local Development Setup

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn src.main:app --reload --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

### Chat Endpoint
```
POST /api/{user_id}/chat
```

**Request Body:**
```json
{
  "conversation_id": 123,
  "message": "Add a task to buy groceries"
}
```

**Response:**
```json
{
  "conversation_id": 123,
  "response": "I've added the task 'buy groceries'",
  "tool_calls": []
}
```

## MCP Tools Available

### add_task
```json
{
  "name": "add_task",
  "parameters": {
    "user_id": "string",
    "title": "string",
    "description": "string (optional)"
  }
}
```

### list_tasks
```json
{
  "name": "list_tasks",
  "parameters": {
    "user_id": "string",
    "status": "string (optional: all|pending|completed)"
  }
}
```

### complete_task
```json
{
  "name": "complete_task",
  "parameters": {
    "user_id": "string",
    "task_id": "integer"
  }
}
```

### delete_task
```json
{
  "name": "delete_task",
  "parameters": {
    "user_id": "string",
    "task_id": "integer"
  }
}
```

### update_task
```json
{
  "name": "update_task",
  "parameters": {
    "user_id": "string",
    "task_id": "integer",
    "title": "string (optional)",
    "description": "string (optional)"
  }
}
```

## Authentication

All API requests must include proper authentication headers from Better Auth. The system will automatically extract the user ID from the authentication token for database queries.

## Database Schema

The system will automatically create the required database tables on startup:
- tasks table: Stores user tasks
- conversations table: Tracks conversation sessions
- messages table: Stores conversation history