# Backend Guidelines - Todo Full-Stack App

**Framework:** FastAPI
**Language:** Python 3.14
**ORM:** SQLModel
**Database:** Neon PostgreSQL
**Authentication:** JWT with bcrypt

---

## Tech Stack

- **FastAPI:** 0.124.0
- **SQLModel:** 0.0.29
- **Uvicorn:** 0.38.0
- **python-jose:** 3.5.0 (JWT)
- **passlib:** 1.7.4 (bcrypt)
- **PostgreSQL Drivers:** psycopg2-binary, asyncpg

---

## Project Structure

```
backend/src/
├── main.py              # FastAPI app entry point
├── api/
│   ├── auth.py         # Authentication endpoints
│   ├── tasks.py        # Task CRUD endpoints
│   └── admin.py        # Admin panel endpoints
├── models/
│   ├── user.py         # User SQLModel
│   └── task.py         # Task SQLModel
├── schemas/
│   ├── auth.py         # Auth Pydantic schemas
│   └── task.py         # Task Pydantic schemas
├── services/
│   ├── user_service.py # User business logic
│   └── task_service.py # Task business logic
├── auth/
│   └── middleware.py   # JWT verification
├── utils/
│   └── password.py     # Password hashing
└── database/
    ├── __init__.py
    └── session.py      # DB connection
```

---

## Database Configuration

### Connection
```python
from sqlmodel import create_engine
import os

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)
```

### Session Management
```python
from sqlmodel import Session

def get_session():
    with Session(engine) as session:
        yield session
```

### Auto-Create Tables
```python
from sqlmodel import SQLModel

# In main.py lifespan
SQLModel.metadata.create_all(bind=engine)
```

---

## API Conventions

### Route Structure
```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/endpoint")
def handler(session: Session = Depends(get_session)):
    # Implementation
    return {"data": result}
```

### Response Format
```python
# Success
return {"message": "Success", "data": result}

# Error
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Resource not found"
)
```

---

## Authentication Patterns

### Password Hashing
```python
from utils.password import hash_password, verify_password

# Hash password on registration
hashed = hash_password("plain_password")

# Verify on login
is_valid = verify_password("plain_password", hashed)
```

### JWT Token Generation
```python
from auth.middleware import create_access_token
from datetime import timedelta

access_token = create_access_token(
    data={"sub": user.email},
    expires_delta=timedelta(minutes=30)
)
```

### Protected Endpoints
```python
from auth.middleware import get_current_user
from typing import Annotated

@router.get("/protected")
def protected_route(
    current_user: Annotated[TokenData, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)]
):
    # current_user.email contains authenticated user
    # Filter queries by user
    pass
```

---

## Database Patterns

### Models (SQLModel)
```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, nullable=False)
    password_hash: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = Field(default=True)
```

### Queries
```python
from sqlmodel import select

# Get all
users = session.exec(select(User)).all()

# Filter
user = session.exec(select(User).where(User.email == email)).first()

# Create
new_user = User(email=email, password_hash=hashed)
session.add(new_user)
session.commit()
session.refresh(new_user)

# Update
user.email = new_email
session.add(user)
session.commit()

# Delete
session.delete(user)
session.commit()
```

---

## Service Layer Pattern

### User Service Example
```python
from models.user import User
from utils.password import hash_password
from sqlmodel import Session, select

def create_user(session: Session, user_data):
    """Create new user with hashed password."""
    hashed_password = hash_password(user_data.password)

    db_user = User(
        email=user_data.email,
        password_hash=hashed_password
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user
```

### Task Service Example
```python
def get_user_tasks(session: Session, user_id: int):
    """Get all tasks for a specific user."""
    tasks = session.exec(
        select(Task).where(Task.user_id == user_id)
    ).all()
    return tasks
```

---

## Security Best Practices

### Always Filter by User
```python
# Good - user-scoped query
tasks = session.exec(
    select(Task).where(Task.user_id == current_user_id)
).all()

# Bad - returns all users' tasks
tasks = session.exec(select(Task)).all()
```

### Validate Ownership
```python
task = session.get(Task, task_id)
if not task or task.user_id != current_user_id:
    raise HTTPException(status_code=404, detail="Task not found")
```

### Never Return Passwords
```python
# Good - exclude password from response
class UserRead(SQLModel):
    id: int
    email: str
    created_at: datetime
    # No password_hash field

# Bad - exposes password hash
return user  # includes password_hash
```

---

## Error Handling

### HTTP Exceptions
```python
from fastapi import HTTPException, status

# 400 Bad Request
raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid input"
)

# 401 Unauthorized
raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"}
)

// 404 Not Found
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Resource not found"
)
```

### Try-Except Patterns
```python
try:
    # Database operation
    session.add(entity)
    session.commit()
except IntegrityError:
    session.rollback()
    raise HTTPException(
        status_code=400,
        detail="Email already registered"
    )
```

---

## CORS Configuration

### Development CORS
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Environment Variables

### Required Variables
```bash
DATABASE_URL=postgresql://user:pass@host/db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ADMIN_EMAIL=admin@taskflow.com
ADMIN_PASSWORD=your-admin-password
```

### Loading Variables
```python
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
```

---

## Running the Backend

### Development
```bash
cd backend
python -m uvicorn src.main:app --reload --port 8000
```

### Access Points
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

---

## Testing

### Manual API Testing
```bash
# Register user
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"Test@123"}'

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"Test@123"}'

# Get tasks (with token)
curl -X GET http://localhost:8000/tasks \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Using Swagger UI
1. Go to http://localhost:8000/docs
2. Click "Authorize" button
3. Enter: `Bearer YOUR_TOKEN_HERE`
4. Test endpoints interactively

---

## Database Migrations

### Current Approach
- Auto-create tables on startup (development)
- SQLModel.metadata.create_all()

### Production (Future)
```bash
# Use Alembic for migrations
alembic init migrations
alembic revision --autogenerate -m "description"
alembic upgrade head
```

---

## Logging

### Current Setup
```python
# SQLAlchemy logging (enabled with echo=True)
engine = create_engine(DATABASE_URL, echo=True)

# Custom logging
import logging
logger = logging.getLogger(__name__)
logger.info(f"User {user.email} logged in")
```

---

## Common Tasks

### Add New Endpoint
1. Create route in `/api/`
2. Create Pydantic schema in `/schemas/`
3. Add business logic in `/services/`
4. Register router in `main.py` (if new file)
5. Test with curl or Swagger UI

### Add New Model Field
1. Update model in `/models/`
2. Update related schemas in `/schemas/`
3. Restart backend (auto-creates column)
4. Update service layer if needed

### Add Admin Functionality
1. Add endpoint in `/api/admin.py`
2. Use environment variables for config
3. Return clear success/error messages
4. Test with admin credentials

---

## Performance Tips

- Use async/await for I/O operations
- Add database indexes on foreign keys
- Use connection pooling (automatic with SQLModel)
- Enable query result caching if needed
- Use pagination for large result sets

---

## Security Checklist

- ✅ Password hashing with bcrypt
- ✅ JWT tokens with expiration
- ✅ User data filtered by user_id
- ✅ SQL injection prevented (ORM)
- ✅ CORS configured properly
- ✅ Environment variables for secrets
- ✅ No password logging
- ✅ Admin credentials secured

---

**Backend Version:** 2.0
**Last Updated:** December 31, 2025
**Status:** ✅ Complete
