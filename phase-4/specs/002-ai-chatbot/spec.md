# Todo AI Chatbot – Phase III (Basic Level) - Specification

**Project:** Todo AI Chatbot – Phase III (Basic Level)
**Version:** 1.0
**Status:** Draft
**Date:** January 1, 2026
**Development Approach:** Spec-Driven Development with Claude Code & Spec-Kit Plus

---

## Executive Summary

Build an AI-powered Todo chatbot that allows users to manage tasks using natural language. The system follows an Agentic Dev Stack workflow: Write spec → Generate plan → Break into tasks → Implement via Claude Code. The chatbot will use OpenAI Agents SDK with MCP tools to perform all task operations, maintaining conversation state in PostgreSQL while keeping the backend stateless.

---

## Project Overview

### Objective
Create an AI-powered Todo chatbot that enables users to manage their tasks through natural language conversations, using OpenAI Agents SDK and MCP tools for all operations.

### Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | OpenAI ChatKit | Conversational UI |
| **Backend** | FastAPI | Stateless API server |
| **AI Framework** | OpenAI Agents SDK | AI logic and reasoning |
| **MCP Server** | Official MCP SDK | Tool integration |
| **ORM** | SQLModel | Database operations |
| **Database** | Neon Serverless PostgreSQL | Data persistence |
| **Authentication** | Better Auth | User authentication |

---

## Core Requirements

### 1. Functional Requirements

#### 1.1 Conversational Interface
- ✅ **Natural Language Processing:** Users can manage tasks using natural language
- ✅ **Task Creation:** AI agent recognizes requests to add/create/remember tasks
- ✅ **Task Listing:** AI agent responds to requests to show/list tasks
- ✅ **Task Completion:** AI agent recognizes when tasks are done/complete/finished
- ✅ **Task Deletion:** AI agent handles requests to delete/remove/cancel tasks
- ✅ **Task Updates:** AI agent processes requests to change/update/rename tasks

#### 1.2 AI Agent Capabilities
- ✅ **Agent Integration:** Use OpenAI Agents SDK for AI logic
- ✅ **Tool Usage:** Agent must use MCP tools for all task operations
- ✅ **Behavior Rules:** Follow defined agent behavior patterns
- ✅ **Error Handling:** Graceful handling of errors like task not found
- ✅ **Confirmation:** Friendly natural language confirmations

#### 1.3 MCP Integration
- ✅ **MCP Server:** Built using Official MCP SDK
- ✅ **Stateless Tools:** MCP tools must be stateless and store data in DB
- ✅ **Tool Contracts:** Implement all required MCP tools (add, list, complete, delete, update)
- ✅ **Tool Validation:** MCP tools validate all inputs and handle errors

#### 1.4 Data Management
- ✅ **Stateless Backend:** FastAPI backend remains stateless per request
- ✅ **Conversation Persistence:** Conversation state stored in PostgreSQL
- ✅ **Task Management:** All task operations stored in database
- ✅ **Message History:** Complete conversation history maintained

#### 1.5 User Experience
- ✅ **Friendly Responses:** Natural language confirmations and feedback
- ✅ **Error Recovery:** Graceful handling of ambiguous or invalid requests
- ✅ **Task Clarification:** List tasks when requests are ambiguous
- ✅ **Responsive Interface:** Real-time chat interface

---

### 2. Technical Requirements

#### 2.1 API Endpoints

**Chat Endpoint:**
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

#### 2.2 Database Schema

**Tasks Table:**
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

**Conversations Table:**
```sql
CREATE TABLE conversation (
  id SERIAL PRIMARY KEY,
  user_id VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);
```

**Messages Table:**
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

#### 2.3 MCP Tools Specification

**1. add_task**
```json
{
  "name": "add_task",
  "parameters": {
    "user_id": "string (required)",
    "title": "string (required)",
    "description": "string (optional)"
  },
  "returns": {
    "task_id": "integer",
    "status": "string",
    "title": "string"
  }
}
```

**2. list_tasks**
```json
{
  "name": "list_tasks",
  "parameters": {
    "user_id": "string (required)",
    "status": "string (optional: all | pending | completed)"
  },
  "returns": {
    "tasks": "array of task objects"
  }
}
```

**3. complete_task**
```json
{
  "name": "complete_task",
  "parameters": {
    "user_id": "string (required)",
    "task_id": "integer (required)"
  },
  "returns": {
    "task_id": "integer",
    "status": "string",
    "title": "string"
  }
}
```

**4. delete_task**
```json
{
  "name": "delete_task",
  "parameters": {
    "user_id": "string (required)",
    "task_id": "integer (required)"
  },
  "returns": {
    "task_id": "integer",
    "status": "string",
    "title": "string"
  }
}
```

**5. update_task**
```json
{
  "name": "update_task",
  "parameters": {
    "user_id": "string (required)",
    "task_id": "integer (required)",
    "title": "string (optional)",
    "description": "string (optional)"
  },
  "returns": {
    "task_id": "integer",
    "status": "string",
    "title": "string"
  }
}
```

#### 2.4 Security Requirements
- ✅ **User Authentication:** Better Auth integration for user verification
- ✅ **Data Isolation:** User data restricted to authenticated user
- ✅ **Input Validation:** All user inputs validated before processing
- ✅ **SQL Injection Prevention:** SQLModel ORM with parameterized queries
- ✅ **Rate Limiting:** Prevent abuse of AI services

---

### 3. User Interface Requirements

#### 3.1 Chat Interface
- ✅ **Real-time Messaging:** Live chat interface using OpenAI ChatKit
- ✅ **Message History:** Display full conversation history
- ✅ **Typing Indicators:** Show when AI is processing
- ✅ **Error States:** Clear error messages when requests fail
- ✅ **Loading States:** Visual feedback during AI processing

#### 3.2 User Experience Flow
- ✅ **Authentication:** Secure login with Better Auth
- ✅ **Conversation Start:** New or existing conversation selection
- ✅ **Natural Language Input:** Text input for natural language requests
- ✅ **AI Response Display:** Clear display of AI responses and actions
- ✅ **Task Status Indicators:** Visual indicators for task completion

---

## Architecture

### System Architecture
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

### Data Flow
```
1. User sends message → ChatKit → FastAPI
2. FastAPI loads conversation history from DB
3. FastAPI appends user message to DB
4. FastAPI runs OpenAI Agent with MCP tools
5. Agent calls MCP tools for operations
6. MCP tools read/write to PostgreSQL
7. Agent generates response
8. FastAPI stores assistant response in DB
9. FastAPI returns response to ChatKit
```

### Component Architecture
```
frontend/
├── src/
│   ├── app/
│   │   ├── chat/
│   │   │   └── page.tsx        # Chat interface
│   │   ├── layout.tsx          # Root layout
│   │   └── page.tsx            # Landing page
│   ├── components/
│   │   ├── ChatInterface.tsx   # ChatKit wrapper
│   │   └── MessageList.tsx     # Message display
│   └── lib/
│       ├── auth.ts             # Better Auth integration
│       └── api.ts              # API client

backend/
├── src/
│   ├── main.py                 # FastAPI app entry
│   ├── api/
│   │   └── chat.py            # Chat endpoint
│   ├── agents/
│   │   └── todo_agent.py      # OpenAI Agent configuration
│   ├── mcp/
│   │   ├── server.py          # MCP server
│   │   └── tools.py           # MCP tool implementations
│   ├── models/
│   │   ├── task.py            # Task model
│   │   ├── conversation.py    # Conversation model
│   │   └── message.py         # Message model
│   ├── services/
│   │   └── chat_service.py    # Chat business logic
│   ├── auth/
│   │   └── middleware.py      # Authentication middleware
│   └── database/
│       └── session.py         # DB connection

specs/
├── spec.md                    # This specification
├── plan.md                    # Implementation plan
├── tasks.md                   # Task breakdown
└── agent/
    ├── spec.md                # Agent behavior specification
    └── tools.md               # MCP tools specification
```

---

## User Scenarios

### Scenario 1: Adding a Task
**User:** "Add a task to buy groceries"
**System:** "I've added the task 'buy groceries' to your list. Is there anything else I can help you with?"

### Scenario 2: Listing Tasks
**User:** "Show me my tasks"
**System:** "Here are your tasks:
1. buy groceries (pending)
2. call mom (pending)
3. finish report (completed)"

### Scenario 3: Completing a Task
**User:** "I finished buying groceries"
**System:** "Great! I've marked 'buy groceries' as completed. You have 1 task remaining."

### Scenario 4: Updating a Task
**User:** "Change 'buy groceries' to 'buy groceries and cook dinner'"
**System:** "I've updated your task from 'buy groceries' to 'buy groceries and cook dinner'."

### Scenario 5: Deleting a Task
**User:** "Remove the call mom task"
**System:** "I've removed the task 'call mom' from your list."

### Scenario 6: Handling Ambiguous Requests
**User:** "Complete the first task"
**System:** "I see multiple pending tasks: 'buy groceries' and 'call mom'. Could you please specify which one you'd like to complete?"

### Scenario 7: Error Handling
**User:** "Complete task 999"
**System:** "I couldn't find a task with ID 999. Would you like me to show you your current tasks?"

---

## Success Criteria

### Functional Success Criteria
- ✅ Users can add tasks using natural language
- ✅ Users can list tasks with status filtering
- ✅ Users can complete tasks by ID or description
- ✅ Users can delete tasks by ID or description
- ✅ Users can update task titles and descriptions
- ✅ AI provides helpful clarifications for ambiguous requests
- ✅ AI handles errors gracefully with user-friendly messages
- ✅ All conversation history is preserved

### Non-Functional Success Criteria
- ✅ Page load time < 3 seconds
- ✅ AI response time < 5 seconds
- ✅ Database operations complete in < 500ms
- ✅ Mobile responsive (works on phones/tablets)
- ✅ Secure authentication (Better Auth integration)
- ✅ Zero security vulnerabilities (XSS, SQL injection)

### User Experience Success Criteria
- ✅ 90% of users can successfully add a task on first try
- ✅ 95% of users can understand AI responses
- ✅ 85% of users find the natural language interface intuitive
- ✅ Average conversation length of 5+ exchanges per session
- ✅ User satisfaction score > 4.0/5.0

---

## Acceptance Criteria

### User Stories & Acceptance

#### US-01: Natural Language Task Creation
**As a** user
**I want to** add tasks using natural language
**So that** I can quickly create tasks without complex commands

**Acceptance Criteria:**
- ✅ AI recognizes various ways to request task creation ("add", "create", "remember", "don't forget")
- ✅ Task title is extracted from natural language
- ✅ Optional description is captured when provided
- ✅ Task is saved to database with user association
- ✅ User receives confirmation of task creation
- ✅ Error handling when task cannot be parsed

#### US-02: Natural Language Task Listing
**As a** user
**I want to** view my tasks using natural language
**So that** I can see what I need to do

**Acceptance Criteria:**
- ✅ AI recognizes various ways to request task listing ("show", "list", "what do I have", "my tasks")
- ✅ Tasks are filtered by status when specified ("pending", "completed", "all")
- ✅ Tasks are displayed with ID, title, and status
- ✅ Empty state handled gracefully
- ✅ Error handling when database query fails

#### US-03: Natural Language Task Completion
**As a** user
**I want to** mark tasks as complete using natural language
**So that** I can track my progress

**Acceptance Criteria:**
- ✅ AI recognizes various ways to complete tasks ("done", "complete", "finished", "completed")
- ✅ Task can be identified by ID or partial title match
- ✅ Task status is updated in database
- ✅ User receives confirmation of completion
- ✅ Error handling when task not found

#### US-04: Natural Language Task Deletion
**As a** user
**I want to** remove tasks using natural language
**So that** I can clean up my task list

**Acceptance Criteria:**
- ✅ AI recognizes various ways to delete tasks ("delete", "remove", "cancel", "get rid of")
- ✅ Task can be identified by ID or partial title match
- ✅ Task is removed from database
- ✅ User receives confirmation of deletion
- ✅ Error handling when task not found

#### US-05: Natural Language Task Updates
**As a** user
**I want to** modify tasks using natural language
**So that** I can keep my tasks up to date

**Acceptance Criteria:**
- ✅ AI recognizes various ways to update tasks ("change", "update", "rename", "modify")
- ✅ Task can be identified by ID or partial title match
- ✅ Task properties (title, description) can be updated
- ✅ Updated task is saved to database
- ✅ User receives confirmation of update
- ✅ Error handling when task not found

#### US-06: Conversation History Persistence
**As a** user
**I want** my conversation history to be saved
**So that** I can continue conversations across sessions

**Acceptance Criteria:**
- ✅ All user messages are stored in database
- ✅ All AI responses are stored in database
- ✅ Conversation context is maintained across requests
- ✅ Multiple conversations per user are supported
- ✅ Message timestamps are accurate

---

## Implementation Details

### AI Agent Behavior
```
1. When user says "add/create/remember":
   - Call add_task MCP tool
   - Confirm task creation to user

2. When user says "show/list":
   - Call list_tasks MCP tool
   - Format and display tasks to user

3. When user says "done/complete/finished":
   - Call complete_task MCP tool
   - Confirm completion to user

4. When user says "delete/remove/cancel":
   - Call delete_task MCP tool
   - Confirm deletion to user

5. When user says "change/update/rename":
   - Call update_task MCP tool
   - Confirm update to user

6. When request is ambiguous:
   - Call list_tasks first to clarify
   - Ask user to be more specific

7. Always respond in friendly natural language
8. Handle errors gracefully with helpful messages
```

### Conversation Flow (Stateless)
```
1. Receive user message
2. Load conversation history from DB
3. Append new user message to DB
4. Run OpenAI Agent with MCP tools
5. Execute MCP tool calls (read/write to DB)
6. Generate AI response
7. Store assistant response in DB
8. Return response to client
9. Server holds no memory between requests
```

### MCP Tool Implementation
Each MCP tool must:
- Be stateless (no server-side state)
- Validate all inputs
- Store data in PostgreSQL
- Return appropriate responses
- Handle errors gracefully

---

## Configuration

### Environment Variables

**Backend .env:**
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

**Frontend .env.local:**
```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_BASE_URL=http://localhost:3000
```

---

## Testing & Validation

### Test Cases
1. ✅ User can add tasks with natural language
2. ✅ User can list all tasks
3. ✅ User can list tasks by status
4. ✅ User can complete tasks
5. ✅ User can delete tasks
6. ✅ User can update tasks
7. ✅ AI handles ambiguous requests by listing tasks
8. ✅ AI provides helpful error messages
9. ✅ Conversation history persists correctly
10. ✅ Multiple users can use the system concurrently

### Performance Metrics
- AI Response Time: < 5 seconds average ✅
- Database Query Time: < 500ms average ✅
- Page Load Time: < 3 seconds ✅
- Concurrent Users: Tested with 10+ users ✅

---

## Deployment Configuration

### Development Setup
```bash
# Backend
cd backend
pip install -r requirements.txt
python -m uvicorn src.main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev
```

### Production Considerations
- Use environment-specific .env files
- Enable HTTPS/SSL
- Configure production CORS origins
- Set up proper logging
- Implement monitoring and alerting
- Scale database connections appropriately
- Set up CDN for static assets

---

## Constraints & Assumptions

### Constraints
- OpenAI API usage costs must be monitored
- MCP SDK is required for tool integration
- Better Auth is required for authentication
- Neon PostgreSQL is required for database

### Assumptions
- Users have stable internet connection
- OpenAI API is available and responsive
- Better Auth provides reliable authentication
- Users are familiar with chat interfaces

---

## Future Enhancements (Out of Scope for Phase III)

### Planned for Phase IV
- Voice input integration
- Task categorization and priorities
- Due dates and reminders
- Task sharing and collaboration
- Advanced AI capabilities (summarization, scheduling)
- Offline functionality
- Mobile app (React Native)

---

## Glossary

- **MCP:** Model Context Protocol - Framework for tool integration
- **AI Agent:** OpenAI Agents SDK - AI system that uses tools
- **ChatKit:** OpenAI's chat interface library
- **Better Auth:** Authentication framework
- **Stateless:** Server doesn't maintain session state between requests
- **SQLModel:** Python SQL ORM framework

---

**Specification Version:** 1.0
**Last Updated:** January 1, 2026
**Author:** Claude Code with Spec-Kit Plus
**Status:** Ready for Planning