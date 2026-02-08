# Todo AI Chatbot – Phase III (Basic Level)

AI-powered Todo chatbot that allows users to manage tasks using natural language. The system follows an Agentic Dev Stack workflow: Write spec → Generate plan → Break into tasks → Implement via Claude Code. The chatbot uses OpenAI Agents SDK with MCP tools to perform all task operations, maintaining conversation state in PostgreSQL while keeping the backend stateless.

## Features

- **Natural Language Processing**: Users can manage tasks using conversational language
- **AI-Powered**: OpenAI Agents SDK with MCP tools for task operations
- **Stateless Architecture**: FastAPI backend with conversation persistence in PostgreSQL
- **Multi-User Support**: User isolation and authentication with Better Auth
- **Real-Time Chat**: Interactive chat interface with typing indicators
- **Complete Task Management**: Add, list, complete, delete, and update tasks

## Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | Next.js 15, OpenAI ChatKit | Conversational UI |
| **Backend** | FastAPI | Stateless API server |
| **AI Framework** | OpenAI Agents SDK | AI logic and reasoning |
| **MCP Server** | Official MCP SDK | Tool integration |
| **ORM** | SQLModel | Database operations |
| **Database** | Neon Serverless PostgreSQL | Data persistence |
| **Authentication** | Better Auth | User authentication |

## Architecture

```
[OpenAI ChatKit UI]
        ↓
[FastAPI Backend (Stateless)]
        ↓
[OpenAI Agents SDK]
        ↓
[MCP Tools Server]
        ↓
[PostgreSQL Database (Neon)]
```

## API Endpoints

### Chat Endpoint
```
POST /api/{user_id}/chat
```

**Request Body:**
```json
{
  "conversation_id": 123,  // Optional: integer
  "message": "Add a task to buy groceries"  // Required: string
}
```

**Response Body:**
```json
{
  "conversation_id": 123,  // Integer
  "response": "I've added the task 'buy groceries'",  // String
  "tool_calls": []  // Array of tool calls executed
}
```

## Database Schema

### Tasks Table
```sql
CREATE TABLE task (
  id SERIAL PRIMARY KEY,
  user_id VARCHAR(255) NOT NULL,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  completed BOOLEAN NOT NULL DEFAULT false,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);
```

### Conversations Table
```sql
CREATE TABLE conversation (
  id SERIAL PRIMARY KEY,
  user_id VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);
```

### Messages Table
```sql
CREATE TABLE message (
  id SERIAL PRIMARY KEY,
  user_id VARCHAR(255) NOT NULL,
  conversation_id INTEGER NOT NULL REFERENCES conversation(id),
  role VARCHAR(20) NOT NULL,  // 'user' or 'assistant'
  content TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL
);
```

## MCP Tools

### add_task
- Accepts: user_id (string), title (string), description (optional string)
- Returns: task_id (integer), status (string), title (string)

### list_tasks
- Accepts: user_id (string), status (optional: all | pending | completed)
- Returns: array of task objects

### complete_task
- Accepts: user_id (string), task_id (integer)
- Returns: task_id (integer), status (string), title (string)

### delete_task
- Accepts: user_id (string), task_id (integer)
- Returns: task_id (integer), status (string), title (string)

### update_task
- Accepts: user_id (string), task_id (integer), title (optional string), description (optional string)
- Returns: task_id (integer), status (string), title (string)

## Setup Instructions

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

### Environment Variables
Create a `.env` file in the backend directory:
```bash
# Database
DATABASE_URL=postgresql://...

# OpenAI
OPENAI_API_KEY=sk-...

# Better Auth
BETTER_AUTH_URL=...
BETTER_AUTH_SECRET=...

# Server
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## Usage Examples

### Adding Tasks
- "Add a task to buy groceries"
- "Create a task to call mom"
- "Remember to finish the report"

### Listing Tasks
- "Show me my tasks"
- "List my pending tasks"
- "What do I have to do?"

### Completing Tasks
- "I finished buying groceries"
- "Complete the call mom task"
- "Mark the report as done"

### Updating Tasks
- "Change 'buy groceries' to 'buy groceries and cook dinner'"
- "Update the description for the report task"

### Deleting Tasks
- "Remove the call mom task"
- "Delete the report task"
- "Cancel the groceries task"

## Development

The project follows the Agentic Dev Stack workflow:
1. Write specification using `/sp.specify`
2. Generate implementation plan using `/sp.plan`
3. Break into tasks using `/sp.tasks`
4. Implement using `/sp.implement`

## License

This project is part of the Todo Evolution series and follows the specification-driven development approach using Claude Code and Spec-Kit Plus.