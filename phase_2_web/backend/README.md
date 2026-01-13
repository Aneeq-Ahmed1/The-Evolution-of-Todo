# FastAPI Todo Backend

This is a secure FastAPI backend for a multi-user Todo application with JWT-based authentication compatible with Better Auth.

## Features

- JWT-based authentication using Better Auth tokens
- User-isolated task management
- Full CRUD operations for tasks
- Proper error handling with consistent response format
- Secure user isolation (users can only access their own tasks)

## Endpoints

### Authentication
All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <JWT_TOKEN>
```

### Task Management

- `GET /api/{user_id}/tasks` - List all tasks for authenticated user
- `POST /api/{user_id}/tasks` - Create new task
- `GET /api/{user_id}/tasks/{id}` - Fetch single task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion status

## Environment Variables

Create a `.env` file with the following variables:

```env
DATABASE_URL=your_neon_postgres_connection_string
BETTER_AUTH_SECRET=your_better_auth_shared_secret
```

## Running the Application

1. Install dependencies: `uv sync`
2. Set up environment variables
3. Run the application: `uv run uvicorn backend.main:app --reload`

## Development

This backend follows the principles of:
- Stateless authentication
- User isolation
- Proper error handling
- Consistent API design