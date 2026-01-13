# API Contracts: FastAPI Backend for Todo Application

**Feature**: 1-fastapi-backend
**Date**: 2026-01-05

## Base Configuration

**Base Path**: `/api`
**Content-Type**: `application/json`
**Authentication**: JWT token in Authorization header (`Authorization: Bearer <token>`)

## Authentication Requirements

All endpoints require a valid JWT token in the Authorization header. The token must:
- Be properly formatted as a JWT
- Have a valid signature using the BETTER_AUTH_SECRET
- Not be expired
- Contain a valid user_id and email

## API Endpoints

### 1. List User Tasks
**Endpoint**: `GET /api/{user_id}/tasks`

**Path Parameters**:
- `user_id` (string): The ID of the user whose tasks to retrieve

**Query Parameters**:
- `status` (string, optional): Filter by completion status
  - Values: "all", "completed", "pending"
  - Default: "all"

**Headers**:
- `Authorization: Bearer <JWT_TOKEN>`
- `Content-Type: application/json`

**Response**:
- Success: `200 OK`
  - Body: Array of task objects
  ```json
  [
    {
      "id": 1,
      "user_id": "user123",
      "title": "Sample task",
      "description": "Sample description",
      "completed": false,
      "created_at": "2026-01-05T10:00:00Z",
      "updated_at": "2026-01-05T10:00:00Z"
    }
  ]
  ```
- Error: `401 Unauthorized` - Invalid or missing token
- Error: `403 Forbidden` - JWT user_id does not match URL user_id
- Error: `422 Validation Error` - Invalid query parameters

### 2. Create Task
**Endpoint**: `POST /api/{user_id}/tasks`

**Path Parameters**:
- `user_id` (string): The ID of the user creating the task

**Headers**:
- `Authorization: Bearer <JWT_TOKEN>`
- `Content-Type: application/json`

**Request Body**:
```json
{
  "title": "Task title",
  "description": "Optional task description"
}
```

**Validation**:
- `title`: Required, 1-200 characters
- `description`: Optional, max 1000 characters

**Response**:
- Success: `201 Created`
  - Body: Created task object
  ```json
  {
    "id": 1,
    "user_id": "user123",
    "title": "Task title",
    "description": "Optional task description",
    "completed": false,
    "created_at": "2026-01-05T10:00:00Z",
    "updated_at": "2026-01-05T10:00:00Z"
  }
  ```
- Error: `401 Unauthorized` - Invalid or missing token
- Error: `403 Forbidden` - JWT user_id does not match URL user_id
- Error: `422 Validation Error` - Invalid request body
- Error: `409 Conflict` - If user validation applies

### 3. Get Single Task
**Endpoint**: `GET /api/{user_id}/tasks/{id}`

**Path Parameters**:
- `user_id` (string): The ID of the user
- `id` (integer): The ID of the task

**Headers**:
- `Authorization: Bearer <JWT_TOKEN>`
- `Content-Type: application/json`

**Response**:
- Success: `200 OK`
  - Body: Task object
  ```json
  {
    "id": 1,
    "user_id": "user123",
    "title": "Sample task",
    "description": "Sample description",
    "completed": false,
    "created_at": "2026-01-05T10:00:00Z",
    "updated_at": "2026-01-05T10:00:00Z"
  }
  ```
- Error: `401 Unauthorized` - Invalid or missing token
- Error: `403 Forbidden` - JWT user_id does not match URL user_id or task doesn't belong to user
- Error: `404 Not Found` - Task does not exist
- Error: `422 Validation Error` - Invalid path parameters

### 4. Update Task
**Endpoint**: `PUT /api/{user_id}/tasks/{id}`

**Path Parameters**:
- `user_id` (string): The ID of the user
- `id` (integer): The ID of the task

**Headers**:
- `Authorization: Bearer <JWT_TOKEN>`
- `Content-Type: application/json`

**Request Body**:
```json
{
  "title": "Updated task title",
  "description": "Updated task description",
  "completed": true
}
```

**Validation**:
- `title`: Required, 1-200 characters
- `description`: Optional, max 1000 characters
- `completed`: Optional, boolean

**Response**:
- Success: `200 OK`
  - Body: Updated task object
  ```json
  {
    "id": 1,
    "user_id": "user123",
    "title": "Updated task title",
    "description": "Updated task description",
    "completed": true,
    "created_at": "2026-01-05T10:00:00Z",
    "updated_at": "2026-01-05T11:00:00Z"
  }
  ```
- Error: `401 Unauthorized` - Invalid or missing token
- Error: `403 Forbidden` - JWT user_id does not match URL user_id or task doesn't belong to user
- Error: `404 Not Found` - Task does not exist
- Error: `422 Validation Error` - Invalid request body or path parameters

### 5. Delete Task
**Endpoint**: `DELETE /api/{user_id}/tasks/{id}`

**Path Parameters**:
- `user_id` (string): The ID of the user
- `id` (integer): The ID of the task to delete

**Headers**:
- `Authorization: Bearer <JWT_TOKEN>`

**Response**:
- Success: `204 No Content` - Task successfully deleted
- Error: `401 Unauthorized` - Invalid or missing token
- Error: `403 Forbidden` - JWT user_id does not match URL user_id or task doesn't belong to user
- Error: `404 Not Found` - Task does not exist
- Error: `422 Validation Error` - Invalid path parameters

### 6. Toggle Task Completion
**Endpoint**: `PATCH /api/{user_id}/tasks/{id}/complete`

**Path Parameters**:
- `user_id` (string): The ID of the user
- `id` (integer): The ID of the task to toggle

**Headers**:
- `Authorization: Bearer <JWT_TOKEN>`

**Request Body**: (Optional)
```json
{
  "completed": true
}
```

**Response**:
- Success: `200 OK`
  - Body: Updated task object with toggled completion status
  ```json
  {
    "id": 1,
    "user_id": "user123",
    "title": "Sample task",
    "description": "Sample description",
    "completed": true,
    "created_at": "2026-01-05T10:00:00Z",
    "updated_at": "2026-01-05T11:00:00Z"
  }
  ```
- Error: `401 Unauthorized` - Invalid or missing token
- Error: `403 Forbidden` - JWT user_id does not match URL user_id or task doesn't belong to user
- Error: `404 Not Found` - Task does not exist
- Error: `422 Validation Error` - Invalid path parameters

## Error Response Format

All error responses follow a consistent format:

```json
{
  "detail": "Error message describing the issue"
}
```

## Authentication Flow

1. User authenticates via Better Auth on the frontend
2. Better Auth issues a JWT token
3. Frontend includes JWT in Authorization header for all API requests
4. Backend verifies JWT signature using BETTER_AUTH_SECRET
5. Backend extracts user_id from JWT and validates against URL user_id
6. Backend processes request if authentication and authorization succeed