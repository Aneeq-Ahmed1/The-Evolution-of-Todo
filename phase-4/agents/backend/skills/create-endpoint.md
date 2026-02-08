# Backend Skill: Create Endpoint

## Skill Name
`create-endpoint`

## Description
Generate a new API endpoint with proper structure, authentication, and error handling.

## Usage
```
/backend:create-endpoint <endpoint-name> <method> [--auth] [--user-scoped]
```

## Examples

```bash
# Create a simple GET endpoint
/backend:create-endpoint get-stats GET

# Create an authenticated POST endpoint
/backend:create-endpoint create-comment POST --auth

# Create user-scoped endpoint
/backend:create-endpoint get-user-posts GET --auth --user-scoped
```

## Parameters

- `<endpoint-name>`: Name of the endpoint (kebab-case)
- `<method>`: HTTP method (GET, POST, PUT, DELETE, PATCH)
- `--auth`: Add authentication requirement
- `--user-scoped`: Filter results by current user

## What It Generates

### 1. API Route (`src/api/<resource>.py`)
```python
@router.get("/resource/{id}")
def get_resource(
    id: int,
    current_user: Annotated[TokenData, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)]
):
    """
    Endpoint description
    """
    # Implementation
    pass
```

### 2. Pydantic Schema (`src/schemas/<resource>.py`)
```python
class ResourceCreate(SQLModel):
    field: str

class ResourceRead(SQLModel):
    id: int
    field: str
    created_at: datetime
```

### 3. Service Function (`src/services/<resource>_service.py`)
```python
def get_resource(session: Session, resource_id: int, user_id: int):
    """
    Business logic for getting resource
    """
    statement = select(Resource).where(
        Resource.id == resource_id,
        Resource.user_id == user_id
    )
    return session.exec(statement).first()
```

### 4. Test Stub (`tests/unit/test_<resource>.py`)
```python
def test_get_resource():
    # Test implementation
    pass
```

## Generated File Structure

```
backend/src/
├── api/
│   └── new_resource.py          # ← New endpoint
├── schemas/
│   └── new_resource.py          # ← Request/Response schemas
├── services/
│   └── new_resource_service.py  # ← Business logic
└── tests/unit/
    └── test_new_resource.py     # ← Tests
```

## Automatic Features

- ✅ Proper error handling (404, 401, 400)
- ✅ Type hints and validation
- ✅ Authentication if `--auth` flag used
- ✅ User scoping if `--user-scoped` flag used
- ✅ Docstrings and comments
- ✅ Consistent naming conventions
- ✅ OpenAPI documentation tags

## Post-Creation Steps

1. Review generated code
2. Implement business logic in service
3. Add validation rules to schema
4. Write tests
5. Register router in `main.py` if new file
6. Test endpoint with curl or Swagger UI

## Example Output

```
✓ Created API route: src/api/comments.py
✓ Created schema: src/schemas/comment.py
✓ Created service: src/services/comment_service.py
✓ Created tests: tests/unit/test_comments.py

Next steps:
1. Implement business logic in comment_service.py
2. Update schema validation in comment.py
3. Add router to main.py:
   from .api.comments import router as comments_router
   app.include_router(comments_router)
4. Test endpoint: curl -X POST http://localhost:8000/comments
```

## Best Practices

- Use descriptive endpoint names
- Follow RESTful conventions
- Add proper validation
- Write comprehensive tests
- Document with docstrings
- Handle errors gracefully

## Related Skills

- `test-endpoint` - Test the new endpoint
- `create-model` - Create database model
- `check-auth` - Verify authentication works
