# API Contract: Phase 2 Web Application

## Overview
This document defines the API contract for the Phase 2 web application backend. The API follows REST principles with JWT authentication for all protected endpoints.

## Base URL
```
http://localhost:8000/api
```

## Authentication
All protected endpoints require JWT authentication in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

## Common Response Format

### Success Response
```json
{
  "data": { /* response data */ },
  "message": "success message"
}
```

### Error Response
```json
{
  "detail": "error message"
}
```

## Authentication Endpoints

### Register User
```
POST /auth/register
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "secure_password_123"
}
```

**Response (201 Created):**
```json
{
  "access_token": "jwt_token_here",
  "token_type": "bearer"
}
```

**Errors:**
- 409: User already exists
- 422: Validation error

### Login User
```
POST /auth/login
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "secure_password_123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "jwt_token_here",
  "token_type": "bearer"
}
```

**Errors:**
- 401: Invalid credentials
- 422: Validation error

## Task Management Endpoints

### Get User's Tasks
```
GET /api/tasks
```

**Headers:**
```
Authorization: Bearer <valid_jwt_token>
```

**Response (200 OK):**
```json
[
  {
    "id": "uuid-string",
    "title": "Task title",
    "description": "Task description",
    "completed": false,
    "user_id": "user-uuid",
    "created_at": "2023-01-01T00:00:00",
    "updated_at": "2023-01-01T00:00:00"
  }
]
```

**Errors:**
- 401: Unauthorized (invalid/expired JWT)

### Create Task
```
POST /api/tasks
```

**Headers:**
```
Authorization: Bearer <valid_jwt_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "New task title",
  "description": "Task description (optional)",
  "completed": false
}
```

**Response (201 Created):**
```json
{
  "id": "uuid-string",
  "title": "New task title",
  "description": "Task description (optional)",
  "completed": false,
  "user_id": "user-uuid",
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-01T00:00:00"
}
```

**Errors:**
- 401: Unauthorized
- 422: Validation error

### Update Task
```
PUT /api/tasks/{task_id}
```

**Headers:**
```
Authorization: Bearer <valid_jwt_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "Updated task title (optional)",
  "description": "Updated description (optional)",
  "completed": true
}
```

**Response (200 OK):**
```json
{
  "id": "uuid-string",
  "title": "Updated task title",
  "description": "Updated description",
  "completed": true,
  "user_id": "user-uuid",
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-01T00:00:00"
}
```

**Errors:**
- 401: Unauthorized
- 403: Task doesn't belong to user
- 404: Task not found
- 422: Validation error

### Delete Task
```
DELETE /api/tasks/{task_id}
```

**Headers:**
```
Authorization: Bearer <valid_jwt_token>
```

**Response (204 No Content):**
Empty response body

**Errors:**
- 401: Unauthorized
- 403: Task doesn't belong to user
- 404: Task not found

### Toggle Task Completion
```
PATCH /api/tasks/{task_id}/toggle
```

**Headers:**
```
Authorization: Bearer <valid_jwt_token>
```

**Response (200 OK):**
```json
{
  "id": "uuid-string",
  "title": "Task title",
  "description": "Task description",
  "completed": true,
  "user_id": "user-uuid",
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-01T00:00:00"
}
```

**Errors:**
- 401: Unauthorized
- 403: Task doesn't belong to user
- 404: Task not found

## Validation Rules

### User Registration/Login
- Email: Valid email format (required)
- Password: Minimum length 8 characters (required)

### Task Creation/Update
- Title: 1-200 characters (required)
- Description: Max 1000 characters (optional)
- Completed: Boolean (default: false)

## Error Codes
- 200: Success
- 201: Created
- 204: No Content
- 401: Unauthorized (invalid/expired JWT)
- 403: Forbidden (user_id mismatch)
- 404: Not Found (resource doesn't exist)
- 409: Conflict (duplicate user)
- 422: Validation Error (invalid request)
- 500: Internal Server Error