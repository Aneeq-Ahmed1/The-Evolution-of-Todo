# API Contract: AI Task Display Mapping

**Feature**: 001-ai-task-mapping
**Date**: 2026-01-04
**Status**: Design

## Overview

This contract defines the API endpoints and data schemas for the task display mapping functionality, enabling ordinal task references (e.g., "task 1 is complete", "edit task 2") to work correctly by mapping displayed task numbers to internal task IDs.

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

### 1. Get All Tasks with Display Indices
```
GET /tasks
```

#### Description
Retrieve all tasks for the authenticated user with display indices for ordinal reference mapping.

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
      "display_index": "number",
      "title": "string",
      "description": "string | null",
      "completed": "boolean",
      "created_at": "string (ISO 8601 timestamp)",
      "updated_at": "string (ISO 8601 timestamp)"
    }
  ],
  "display_mapping": [
    {
      "display_index": "number",
      "task_id": "string"
    }
  ]
}
```

- **Error (401)**: Unauthorized
- **Error (500)**: Internal server error

### 2. Get Task by Display Index
```
GET /tasks/display/{display_index}
```

#### Description
Retrieve a specific task by its display index (1-based).

#### Request
- **Headers**:
  - `Authorization: Bearer <jwt-token>`
- **Parameters**:
  - `display_index: number (required)`
- **Body**: None

#### Response
- **Success (200)**:
```json
{
  "task_id": "string",
  "display_index": "number",
  "title": "string",
  "description": "string | null",
  "completed": "boolean",
  "created_at": "string (ISO 8601 timestamp)",
  "updated_at": "string (ISO 8601 timestamp)"
}
```

- **Error (401)**: Unauthorized
- **Error (404)**: Task not found at specified display index
- **Error (500)**: Internal server error

### 3. Update Task by Display Index
```
PUT /tasks/display/{display_index}
```

#### Description
Update an existing task using its display index.

#### Request
- **Headers**:
  - `Authorization: Bearer <jwt-token>`
- **Parameters**:
  - `display_index: number (required)`
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
  "display_index": "number",
  "title": "string",
  "description": "string | null",
  "completed": "boolean",
  "created_at": "string (ISO 8601 timestamp)",
  "updated_at": "string (ISO 8601 timestamp)"
}
```

- **Error (400)**: Bad request (validation error)
- **Error (401)**: Unauthorized
- **Error (404)**: Task not found at specified display index
- **Error (500)**: Internal server error

### 4. Delete Task by Display Index
```
DELETE /tasks/display/{display_index}
```

#### Description
Delete a specific task by its display index.

#### Request
- **Headers**:
  - `Authorization: Bearer <jwt-token>`
- **Parameters**:
  - `display_index: number (required)`
- **Body**: None

#### Response
- **Success (204)**: No content (task deleted successfully)
- **Error (401)**: Unauthorized
- **Error (404)**: Task not found at specified display index
- **Error (500)**: Internal server error

### 5. Toggle Task Completion by Display Index
```
PATCH /tasks/display/{display_index}/completion
```

#### Description
Toggle the completion status of a task using its display index.

#### Request
- **Headers**:
  - `Authorization: Bearer <jwt-token>`
- **Parameters**:
  - `display_index: number (required)`
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
  "display_index": "number",
  "title": "string",
  "description": "string | null",
  "completed": "boolean",
  "created_at": "string (ISO 8601 timestamp)",
  "updated_at": "string (ISO 8601 timestamp)"
}
```

- **Error (400)**: Bad request (validation error)
- **Error (401)**: Unauthorized
- **Error (404)**: Task not found at specified display index
- **Error (500)**: Internal server error

### 6. Refresh Display Mapping
```
POST /mapping/refresh
```

#### Description
Refresh the display index to task_id mapping after task list changes.

#### Request
- **Headers**:
  - `Authorization: Bearer <jwt-token>`
- **Parameters**: None
- **Body**:
```json
{
  "user_id": "string (required)",
  "tasks": [
    {
      "id": "string (required)",
      "title": "string (required)",
      "completed": "boolean (required)"
    }
  ]
}
```

#### Response
- **Success (200)**:
```json
{
  "mapping_updated": "boolean",
  "total_mappings": "number",
  "display_mapping": [
    {
      "display_index": "number",
      "task_id": "string"
    }
  ],
  "refreshed_at": "string (ISO 8601 timestamp)"
}
```

- **Error (400)**: Bad request (validation error)
- **Error (401)**: Unauthorized
- **Error (500)**: Internal server error

### 7. Resolve Display Index to Task ID
```
POST /mapping/resolve
```

#### Description
Resolve a display index to its corresponding task ID.

#### Request
- **Headers**:
  - `Authorization: Bearer <jwt-token>`
- **Parameters**: None
- **Body**:
```json
{
  "display_index": "number (required)",
  "user_id": "string (required)"
}
```

#### Response
- **Success (200)**:
```json
{
  "task_id": "string",
  "display_index": "number",
  "valid": "boolean",
  "error": "string (optional)"
}
```

- **Error (400)**: Bad request (validation error)
- **Error (401)**: Unauthorized
- **Error (500)**: Internal server error

## Data Schemas

### Task with Display Index Object
```json
{
  "task_id": {
    "type": "string",
    "required": true,
    "description": "Internal unique identifier for the task"
  },
  "display_index": {
    "type": "number",
    "required": true,
    "minimum": 1,
    "description": "Display index for ordinal references (1-based)"
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

### Display Mapping Object
```json
{
  "display_index": {
    "type": "number",
    "required": true,
    "minimum": 1,
    "description": "Display index (1-based) shown to user"
  },
  "task_id": {
    "type": "string",
    "required": true,
    "description": "Internal task identifier"
  }
}
```

### Refresh Mapping Request
```json
{
  "user_id": {
    "type": "string",
    "required": true,
    "description": "User identifier for mapping context"
  },
  "tasks": {
    "type": "array",
    "required": true,
    "items": {
      "type": "object",
      "properties": {
        "id": {"type": "string", "required": true},
        "title": {"type": "string", "required": true},
        "completed": {"type": "boolean", "required": true}
      }
    }
  }
}
```

### Error Response
```json
{
  "detail": {
    "type": "string",
    "required": true,
    "description": "Error message describing the issue"
  }
}
```

## AI Agent Integration Points

### Ordinal Reference Patterns
The AI agent should recognize these patterns and extract the display index:
- "task {number}" → e.g., "task 1", "task 2"
- "number {number}" → e.g., "number 1 task", "number 2 task"
- "{ordinal} task" → e.g., "first task", "second task", "third task"
- "{number}st/nd/rd/th task" → e.g., "1st task", "2nd task", "3rd task", "4th task"

### Intent Mapping
- **Complete Task**: "task 1 is complete", "complete task 2", "task 3 is done"
- **Edit Task**: "edit task 1", "update task 2", "change task 3"
- **Delete Task**: "delete task 1", "remove task 2", "task 3 is not needed"
- **Uncomplete Task**: "uncomplete task 1", "make task 2 incomplete"

## Validation Rules

### Request Validation
- `display_index` must be a positive integer ≥ 1
- `display_index` must exist in current user's display mapping
- `task_id` must be a valid identifier in the system
- `title` must be 1-255 characters when provided
- `description` must be 0-1000 characters when provided
- `completed` must be a boolean value
- All requests must include valid JWT token

### Response Validation
- Success responses must include complete task object with updated `updated_at`
- Error responses must follow the standard error format
- Display indices must be sequential starting from 1
- Timestamps must be in ISO 8601 format