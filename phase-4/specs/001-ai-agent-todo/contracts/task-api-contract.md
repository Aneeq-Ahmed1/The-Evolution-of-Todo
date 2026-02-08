# API Contract: Task Management Operations

**Feature**: 001-ai-agent-todo
**Date**: 2026-01-04
**Status**: Design

## Overview

This contract defines the API endpoints and data schemas for task management operations, specifically focusing on edit, delete, update, and completion toggle functionality that integrates with the AI agent.

## Base URL
```
http://localhost:8000 (development)
https://[production-domain]/api (production)
```

## Authentication
All endpoints require JWT authentication in the Authorization header:
```
Authorization: Bearer <jwt-token>
```

## Endpoints

### 1. Get All Tasks
```
GET /tasks
```

#### Description
Retrieve all tasks for the authenticated user.

#### Request
- **Headers**:
  - `Authorization: Bearer <jwt-token>`
- **Parameters**: None
- **Body**: None

#### Response
- **Success (200)**:
```json
{
  "tasks": [
    {
      "task_id": "string",
      "title": "string",
      "description": "string | null",
      "completed": "boolean",
      "created_at": "string (ISO 8601 timestamp)",
      "updated_at": "string (ISO 8601 timestamp)"
    }
  ]
}
```

- **Error (401)**: Unauthorized
- **Error (500)**: Internal server error

### 2. Create Task
```
POST /tasks
```

#### Description
Create a new task for the authenticated user.

#### Request
- **Headers**:
  - `Authorization: Bearer <jwt-token>`
- **Parameters**: None
- **Body**:
```json
{
  "title": "string (required)",
  "description": "string (optional, default: null)",
  "completed": "boolean (optional, default: false)"
}
```

#### Response
- **Success (201)**:
```json
{
  "task_id": "string",
  "title": "string",
  "description": "string | null",
  "completed": "boolean",
  "created_at": "string (ISO 8601 timestamp)",
  "updated_at": "string (ISO 8601 timestamp)"
}
```

- **Error (400)**: Bad request (validation error)
- **Error (401)**: Unauthorized
- **Error (500)**: Internal server error

### 3. Get Task by ID
```
GET /tasks/{task_id}
```

#### Description
Retrieve a specific task by its ID.

#### Request
- **Headers**:
  - `Authorization: Bearer <jwt-token>`
- **Parameters**:
  - `task_id: string (required)`
- **Body**: None

#### Response
- **Success (200)**:
```json
{
  "task_id": "string",
  "title": "string",
  "description": "string | null",
  "completed": "boolean",
  "created_at": "string (ISO 8601 timestamp)",
  "updated_at": "string (ISO 8601 timestamp)"
}
```

- **Error (401)**: Unauthorized
- **Error (404)**: Task not found
- **Error (500)**: Internal server error

### 4. Update Task
```
PUT /tasks/{task_id}
```

#### Description
Update an existing task with new title and/or description.

#### Request
- **Headers**:
  - `Authorization: Bearer <jwt-token>`
- **Parameters**:
  - `task_id: string (required)`
- **Body**:
```json
{
  "title": "string (optional)",
  "description": "string (optional)"
}
```

#### Response
- **Success (200)**:
```json
{
  "task_id": "string",
  "title": "string",
  "description": "string | null",
  "completed": "boolean",
  "created_at": "string (ISO 8601 timestamp)",
  "updated_at": "string (ISO 8601 timestamp)"
}
```

- **Error (400)**: Bad request (validation error)
- **Error (401)**: Unauthorized
- **Error (404)**: Task not found
- **Error (500)**: Internal server error

### 5. Delete Task
```
DELETE /tasks/{task_id}
```

#### Description
Delete a specific task by its ID.

#### Request
- **Headers**:
  - `Authorization: Bearer <jwt-token>`
- **Parameters**:
  - `task_id: string (required)`
- **Body**: None

#### Response
- **Success (204)**: No content (task deleted successfully)
- **Error (401)**: Unauthorized
- **Error (404)**: Task not found
- **Error (500)**: Internal server error

### 6. Toggle Task Completion
```
PATCH /tasks/{task_id}
```

#### Description
Toggle the completion status of a task.

#### Request
- **Headers**:
  - `Authorization: Bearer <jwt-token>`
- **Parameters**:
  - `task_id: string (required)`
- **Body**:
```json
{
  "completed": "boolean (required)"
}
```

#### Response
- **Success (200)**:
```json
{
  "task_id": "string",
  "title": "string",
  "description": "string | null",
  "completed": "boolean",
  "created_at": "string (ISO 8601 timestamp)",
  "updated_at": "string (ISO 8601 timestamp)"
}
```

- **Error (400)**: Bad request (validation error)
- **Error (401)**: Unauthorized
- **Error (404)**: Task not found
- **Error (500)**: Internal server error

## Data Schemas

### Task Object
```json
{
  "task_id": {
    "type": "string",
    "required": true,
    "description": "Unique identifier for the task, persists throughout task lifecycle"
  },
  "title": {
    "type": "string",
    "required": true,
    "minLength": 1,
    "maxLength": 255,
    "description": "Task title, required for all tasks"
  },
  "description": {
    "type": ["string", "null"],
    "required": false,
    "maxLength": 1000,
    "description": "Optional task description"
  },
  "completed": {
    "type": "boolean",
    "required": true,
    "default": false,
    "description": "Task completion status"
  },
  "created_at": {
    "type": "string",
    "format": "date-time",
    "required": true,
    "description": "Timestamp when task was created"
  },
  "updated_at": {
    "type": "string",
    "format": "date-time",
    "required": true,
    "description": "Timestamp when task was last updated"
  }
}
```

### Error Response
```json
{
  "detail": "string (error message)"
}
```

## AI Agent Integration Points

### Intent Mapping
The AI agent should map these user intents to specific API calls:
- "Edit task [title/description]" → `PUT /tasks/{task_id}`
- "Delete task [title]" → `DELETE /tasks/{task_id}`
- "Complete task [title]" → `PATCH /tasks/{task_id}` with `completed: true`
- "Uncomplete task [title]" → `PATCH /tasks/{task_id}` with `completed: false`
- "Update task [title]" → `PUT /tasks/{task_id}`

### Task Identification
The AI agent must extract the correct `task_id` from user context to ensure operations target the intended task.

## Validation Rules

### Request Validation
- `task_id` must be a valid identifier in the system
- `title` must be 1-255 characters when provided
- `description` must be 0-1000 characters when provided
- `completed` must be a boolean value
- All requests must include valid JWT token

### Response Validation
- Success responses must include complete task object with updated `updated_at`
- Error responses must follow the standard error format
- Timestamps must be in ISO 8601 format