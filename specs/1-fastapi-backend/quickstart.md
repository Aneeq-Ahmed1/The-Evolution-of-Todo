# Quickstart Guide: FastAPI Todo Backend

## Prerequisites

- Python 3.11+
- uv (dependency manager)

## Setup

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Set up environment variables:**
   Create a `.env` file with:
   ```env
   DATABASE_URL=postgresql://user:password@localhost/todo_db
   BETTER_AUTH_SECRET=your_better_auth_shared_secret
   ```

3. **Run the application:**
   ```bash
   uv run uvicorn backend.main:app --reload
   ```

## Testing the API

The API will be available at `http://localhost:8000`.

### Authentication

All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <JWT_TOKEN>
```

### Testing Endpoints

1. **Create a task:**
   ```bash
   curl -X POST http://localhost:8000/api/user123/tasks \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"title": "Test task", "description": "Test description"}'
   ```

2. **List tasks:**
   ```bash
   curl -X GET http://localhost:8000/api/user123/tasks \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
   ```

3. **Get a specific task:**
   ```bash
   curl -X GET http://localhost:8000/api/user123/tasks/1 \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
   ```

4. **Update a task:**
   ```bash
   curl -X PUT http://localhost:8000/api/user123/tasks/1 \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"title": "Updated task", "completed": true}'
   ```

5. **Toggle task completion:**
   ```bash
   curl -X PATCH http://localhost:8000/api/user123/tasks/1/complete \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"completed": true}'
   ```

6. **Delete a task:**
   ```bash
   curl -X DELETE http://localhost:8000/api/user123/tasks/1 \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
   ```

## API Documentation

Interactive API documentation is available at:
- `http://localhost:8000/docs` (Swagger UI)
- `http://localhost:8000/redoc` (ReDoc)

## Validation

All functionality has been validated to ensure:
- JWT authentication works correctly
- User isolation is enforced (users can only access their own tasks)
- All CRUD operations work as expected
- Error handling provides appropriate HTTP status codes
- Input validation works correctly