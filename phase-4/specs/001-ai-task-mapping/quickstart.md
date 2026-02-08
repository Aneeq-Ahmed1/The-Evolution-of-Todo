# Quickstart Guide: AI Task Display Mapping

**Feature**: 001-ai-task-mapping
**Date**: 2026-01-04
**Status**: Implementation Ready

## Overview

This guide provides setup and development instructions for implementing AI-driven task ordinal reference functionality, enabling commands like "task 1 is complete" and "edit task 2" to work correctly by mapping displayed task numbers to internal task IDs.

## Prerequisites

### Development Environment
- Node.js 18+ (for frontend development)
- Python 3.11+ (for backend development)
- Git for version control
- Access to Neon PostgreSQL database
- Access to AI agent integration service

### Required Dependencies
- Backend: FastAPI, SQLModel, python-jose, passlib[bcrypt], psycopg2-binary
- Frontend: Next.js 15+, React 18+, TypeScript, Tailwind CSS
- Development: uv, pytest, jest

## Setup Instructions

### 1. Clone and Initialize Repository
```bash
# Clone the repository
git clone [repository-url]
cd [repository-name]

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Install frontend dependencies
cd ../frontend
npm install
```

### 2. Environment Configuration
```bash
# Create environment files
cp .env.example .env  # for backend
cp .env.example .env.local  # for frontend

# Configure database connection
DATABASE_URL=postgresql://[user]:[password]@[host]:[port]/[database]

# Configure JWT settings
SECRET_KEY=[your-secret-key]
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Configure API settings
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### 3. Database Setup
```bash
# Start backend to initialize database
cd backend
python -m uvicorn src.main:app --reload --port 8000

# Database tables will be created automatically
# Verify tables exist in Neon dashboard
```

## Development Workflow

### 1. Backend Development
```bash
# Start backend server
cd backend
python -m uvicorn src.main:app --reload --port 8000

# Run backend tests
python -m pytest
```

### 2. Frontend Development
```bash
# Start frontend development server
cd frontend
npm run dev

# Run frontend tests
npm test
```

## Implementation Steps

### Step 1: Runtime Mapping Implementation
1. Create display_index to task_id mapping in the UI layer
2. Pass mapping to AI agent context when task list is displayed
3. Update mapping when task list changes (add/delete/reorder)

### Step 2: AI Agent Enhancement
1. Update natural language processing to recognize ordinal references
2. Extract display_index from user commands containing ordinal references
3. Resolve display_index to internal task_id using runtime mapping
4. Execute backend operations using resolved task_id

### Step 3: Validation and Error Handling
1. Validate that display_index exists in current mapping before resolution
2. Provide helpful error messages for invalid task numbers
3. Ensure AI agent responds confidently when intent is clear

## Key Files to Modify

### Backend Files
```
backend/src/api/tasks.py
backend/src/services/task_service.py
backend/src/models/task.py
backend/src/schemas/task.py
```

### Frontend Files
```
frontend/src/components/TaskList.tsx
frontend/src/services/taskService.ts
frontend/src/app/dashboard/tasks/page.tsx
```

### AI Agent Files
```
agents/backend/src/agents/todo_agent.py
agents/backend/src/services/intent_parser.py
agents/backend/src/services/ordinal_resolver.py
```

## API Endpoints

### Task Operations with Display Index
- `GET /tasks` - Retrieve user's tasks with display indexing
- `PUT /tasks/by-display-index/{display_index}` - Update task by display index
- `DELETE /tasks/by-display-index/{display_index}` - Delete task by display index
- `PATCH /tasks/by-display-index/{display_index}/completion` - Toggle completion by display index

### Mapping Operations
- `POST /mapping/refresh` - Refresh display mapping after task list changes
- `GET /mapping/resolve/{display_index}` - Resolve display index to task ID

### Expected Request/Response Formats

#### Resolve Display Index Request
```json
{
  "display_index": 1,
  "user_id": "user-123"
}
```

#### Resolve Display Index Response
```json
{
  "task_id": "task-456",
  "display_index": 1,
  "valid": true,
  "error": null
}
```

#### Refresh Mapping Request
```json
{
  "user_id": "user-123",
  "tasks": [
    {
      "id": "task-456",
      "title": "Buy groceries",
      "completed": false
    },
    {
      "id": "task-789",
      "title": "Pay bills",
      "completed": true
    }
  ]
}
```

#### Refresh Mapping Response
```json
{
  "mapping_updated": true,
  "total_mappings": 2,
  "display_mapping": [
    { "display_index": 1, "task_id": "task-456" },
    { "display_index": 2, "task_id": "task-789" }
  ],
  "refreshed_at": "2026-01-04T10:00:00Z"
}
```

## Testing Strategy

### 1. Unit Tests
- Test ordinal reference parsing functions
- Verify display_index to task_id resolution
- Test error handling for invalid indices

### 2. Integration Tests
- Test AI agent recognition of ordinal references
- Verify backend API handles display_index parameters correctly
- Test mapping synchronization between UI and AI agent

### 3. End-to-End Tests
- Test complete user workflows with ordinal references
- Verify task operations work with commands like "task 1 is complete"
- Test edge cases and error scenarios

## Common Issues and Solutions

### Issue: Display mapping not synchronizing between UI and AI agent
**Solution**: Ensure mapping is refreshed and shared when task list changes

### Issue: Invalid task number references causing generic errors
**Solution**: Implement proper validation and helpful error messaging

### Issue: Ordinal references not recognized by AI agent
**Solution**: Update natural language processing to include ordinal patterns

### Issue: Mapping becoming stale after task operations
**Solution**: Implement automatic mapping refresh after add/delete/reorder operations

## Deployment Notes

### Environment Variables
- Ensure database connection settings are properly configured
- Set appropriate JWT secret keys for production
- Configure CORS settings for production domain

### Database Migrations
- For production: Implement proper migration strategy
- For development: Auto-create tables on startup is sufficient

## Next Steps

1. Implement runtime display mapping in frontend
2. Update AI agent to recognize ordinal references
3. Create mapping resolution service
4. Test all ordinal reference commands end-to-end
5. Deploy to staging environment for validation