# Backend Development Guidelines

## Project Structure

```
backend/
├── main.py              # FastAPI entry point
├── db.py                # Database connection and session management
├── models.py            # SQLModel database models
├── auth.py              # JWT authentication and verification
├── routes/
│   └── tasks.py         # Task-related API routes
├── schemas.py           # Pydantic request/response models
├── settings.py          # Configuration and environment variables
└── CLAUDE.md            # This file - Backend development guidelines
```

## Development Rules

### 1. Authentication & Security
- All endpoints must require JWT authentication
- JWT tokens must be verified using the BETTER_AUTH_SECRET
- User ID from JWT must match the user ID in the URL
- Never store session data on the server (stateless authentication)

### 2. Database Operations
- Use SQLModel for all database interactions
- Always filter tasks by user_id to ensure user isolation
- Use async database operations where possible
- Handle database errors gracefully

### 3. Error Handling
- Use consistent error response format: `{"detail": "error message"}`
- Return appropriate HTTP status codes:
  - 200: Success
  - 201: Created
  - 204: No Content
  - 401: Unauthorized (invalid/expired JWT)
  - 403: Forbidden (user_id mismatch)
  - 404: Not Found (resource doesn't exist)
  - 409: Conflict (duplicate user)
  - 422: Validation Error (invalid request)

### 4. Validation
- Validate all input data using Pydantic schemas
- Task titles: 1-200 characters
- Task descriptions: max 1000 characters (optional)
- Validate JWT token expiry and signature

### 5. API Design
- Follow RESTful principles
- Base path: `/api`
- All endpoints require `Authorization: Bearer <token>` header
- Content-Type: `application/json`

### 6. Code Organization
- Separate concerns: models, schemas, services, routes, auth
- Use dependency injection for authentication
- Keep route handlers thin - delegate to service layer
- Write async functions for I/O operations