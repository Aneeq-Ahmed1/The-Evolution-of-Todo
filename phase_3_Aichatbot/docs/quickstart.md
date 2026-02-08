# Quickstart Guide: AI-Native Agent Platform

## Overview
This guide will help you set up and run the AI-Native Agent Platform with provider-agnostic interface. The system provides a standardized interface that routes requests to configurable LLM providers while maintaining clean separation of concerns.

## Prerequisites
- Python 3.11+
- Node.js 18+ (for frontend)
- PostgreSQL database (or use SQLite for development)
- API keys for your preferred LLM provider (Google Gemini, OpenAI, etc.)

## Installation

### Backend Setup
1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Copy the example environment file and configure your settings:
```bash
cp .env.example .env
```

4. Edit the `.env` file with your database URL and API keys:
```bash
DATABASE_URL=postgresql://username:password@localhost:5432/ai_agent_db
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
LLM_PROVIDER=gemini  # or openai
SECRET_KEY=your-super-secret-key-change-in-production
```

### Frontend Setup
1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install JavaScript dependencies:
```bash
npm install
```

3. Create a `.env.local` file for frontend environment variables:
```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## Running the Application

### Backend
1. Start the backend server:
```bash
cd backend
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

### Frontend
1. Start the frontend development server:
```bash
cd frontend
npm run dev
```

The frontend will be available at `http://localhost:3000`

## API Endpoints

### Chat API
- `POST /api/chat` - Main chat endpoint for AI interactions
- `GET /api/conversations` - Get user's conversations
- `POST /api/conversations` - Create a new conversation
- `GET /api/conversations/{id}` - Get a specific conversation

### MCP Server (Model Context Protocol)
- `POST /api/mcp/tools/call` - Call MCP tools (create_task, list_tasks, etc.)

### Health Checks
- `GET /api/health` - Basic health check
- `GET /api/health/detail` - Detailed health check
- `GET /api/health/ready` - Readiness probe
- `GET /api/health/live` - Liveness probe

## Configuration

### Provider Selection
Configure which LLM provider to use by setting the `LLM_PROVIDER` environment variable:
- `gemini` - Google Gemini
- `openai` - OpenAI GPT models

### Authentication
The system implements JWT-based authentication. Users must provide a valid JWT token in the `Authorization: Bearer <token>` header for authenticated endpoints.

### Rate Limiting
The system implements rate limiting to prevent abuse. Default limits are 100 requests per hour per user.

### Data Retention
Conversations are retained for 30 days by default. This can be configured with the `CONVERSATION_RETENTION_DAYS` environment variable.

## MCP Tools

The system provides several MCP tools that can be called by AI agents:

### Task Management Tools
- `create_task`: Create a new task with title, description, and status
- `list_tasks`: List tasks with optional filtering by status
- `update_task`: Update task properties
- `delete_task`: Delete a task

### Conversation Tools
- `get_conversation_history`: Retrieve conversation history

## Frontend Integration

The frontend provides a ChatKit-based interface that:
- Displays conversation history
- Shows agent and user messages with distinct styling
- Provides loading indicators during AI processing
- Handles errors gracefully

## Development

### Adding New MCP Tools
1. Add a new handler function in `backend/src/api/mcp_server.py`
2. Update the main routing logic to call your new handler
3. Update the available tools list in the metadata

### Extending the Agent System
1. Create new agent classes in `backend/src/agents/`
2. Create new skill classes in `backend/src/skills/`
3. Register them with the orchestrator agent

## Troubleshooting

### Common Issues
- **Database Connection**: Ensure your DATABASE_URL is correctly configured
- **API Keys**: Verify that your LLM provider API keys are valid and properly set
- **Authentication**: Check that JWT tokens are being sent correctly in requests
- **CORS**: If experiencing cross-origin issues, update the CORS middleware settings

### Logging
Check the application logs for detailed error information. The system logs requests and errors for debugging.

## Security Best Practices

- Never hardcode API keys in source code
- Use strong, rotating JWT secrets
- Implement proper rate limiting
- Validate all user inputs
- Regularly update dependencies