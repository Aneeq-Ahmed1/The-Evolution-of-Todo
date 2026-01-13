---
id: 1
title: "FastAPI Backend for Todo Application Specification"
stage: spec
date_iso: "2026-01-05"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "fastapi-backend"
branch: "1-fastapi-backend"
user: "user"
command: "/sp.specify"
labels: ["backend", "fastapi", "todo", "specification"]
links:
  spec: "specs/1-fastapi-backend/spec.md"
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "specs/1-fastapi-backend/spec.md"
  - "specs/1-fastapi-backend/checklists/requirements.md"
  - "history/prompts/general/1-fastapi-backend-specification.general.prompt.md"
tests_yaml: []
---

# FastAPI Backend for Todo Application Specification

## User Input (PROMPT_TEXT)

```
Project Phase: Phase II – Full-Stack Web Application (Backend)

Objective:
Design and specify a Python FastAPI backend that powers a multi-user Todo web application.
The frontend (Next.js 16+ App Router) is already implemented and expects a REST API with JWT-based authentication.
All backend behavior must strictly follow this specification and be compatible with Better Auth issued JWT tokens.

Development Rules:
- No manual coding assumptions
- Backend must work independently from frontend runtime
- JWT verification must be stateless
- Use uv for dependency management
- Python 3.11+

--------------------------------------------------
TECH STACK
--------------------------------------------------
- Framework: FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Auth: Better Auth (JWT issued on frontend)
- Token Verification: PyJWT
- Server: Uvicorn
- Dependency Manager: uv

--------------------------------------------------
AUTHENTICATION & SECURITY
--------------------------------------------------
Authentication Source:
- Authentication is handled on the frontend using Better Auth.
- Better Auth issues JWT tokens on successful login/signup.

JWT Rules:
- Every API request MUST include:
  Authorization: Bearer <JWT_TOKEN>
- Backend must:
  1. Extract JWT from Authorization header
  2. Verify signature using shared secret (BETTER_AUTH_SECRET)
  3. Verify token expiry
  4. Decode user_id and email from token

Shared Secret:
- Environment variable:
  BETTER_AUTH_SECRET=<shared_secret>
- This secret MUST match the frontend Better Auth secret exactly.

Authorization Rules:
- All endpoints are protected
- Requests without valid JWT → 401 Unauthorized
- user_id in URL MUST match user_id in JWT
- If mismatch →tion: Bearer <token>
- Conte 403 Forbidden

Logout Behavior:
- Logout invalidates frontend session ONLY
- Backend MUST NOT delete users or tasks on logout

Duplicate Account Rule:
- Same email MUST NOT be allowed to register twice
- Backend must reject duplicate users if user table is ever referenced
- Expected error: HTTP 409 Conflict

--------------------------------------------------
DATABASE DESIGN (SQLModel)
--------------------------------------------------

Table: tasks

Fields:
- id: int (Primary Key)
- user_id: str (indexed, from JWT)
- title: str (1–200 chars, required)
- description: Optional[str] (max 1000 chars)
- completed: bool (default False)
- created_at: datetime
- updated_at: datetime

Constraints:
- Every task MUST belong to exactly one user
- Queries MUST ALWAYS filter by user_id

Database:
- Neon Serverless PostgreSQL
- Connection string from:
  DATABASE_URL

--------------------------------------------------
API BASE RULES
--------------------------------------------------
Base Path:
- /api

Headers:
- Authorizant-Type: application/json

Response Format:
- JSON only
- Use Pydantic response models
- Consistent error structure

--------------------------------------------------
API ENDPOINTS (FINAL & LOCKED)
--------------------------------------------------

GET /api/{user_id}/tasks
- List all tasks for authenticated user
- Must only return tasks owned by JWT user
- Optional query params:
  - status = all | completed | pending

POST /api/{user_id}/tasks
- Create new task
- Body:
  - title (required)
  - description (optional)
- Task is automatically associated with JWT user

GET /api/{user_id}/tasks/{id}
- Fetch single task
- Must verify task ownership

PUT /api/{user_id}/tasks/{id}
- Update task title/description/completed
- Ownership check required

DELETE /api/{user_id}/tasks/{id}
- Delete task
- Ownership check required

PATCH /api/{user_id}/tasks/{id}/complete
- Toggle completed status
- Ownership check required

--------------------------------------------------
ERROR HANDLING
--------------------------------------------------
401 Unauthorized:
- Missing token
- Invalid token
- Expired token

403 Forbidden:
- JWT user_id ≠ URL user_id
- Accessing another user's task

404 Not Found:
- Task does not exist
- Task does not belong to user

409 Conflict:
- Duplicate email (if user validation applies)

422 Validation Error:
- Invalid request body

--------------------------------------------------
BACKEND PROJECT STRUCTURE
--------------------------------------------------
backend/
├── main.py              # FastAPI entry
├── db.py                # Neon DB connection
├── models.py            # SQLModel models
├── auth.py              # JWT verification dependency
├── routes/
│   └── tasks.py         # All task routes
├── schemas.py           # Pydantic request/response models
├── settings.py          # Env config
└── CLAUDE.md            # Backend rules

--------------------------------------------------
NON-GOALS
--------------------------------------------------
- No frontend code
- No UI logic
- No session storage
- No cookies
- No OAuth
- No admin users

--------------------------------------------------
SUCCESS CRITERIA
--------------------------------------------------
- Backend runs independently on localhost:8000
- All endpoints require JWT
- Tasks are fully user-isolated
- Duplicate signup bug is impossible
- Logout does NOT delete user data
- Compatible with existing Next.js frontend

End of specification.
```

## Assistant Response (RESPONSE_TEXT)

Created a comprehensive feature specification for a FastAPI backend for a multi-user Todo web application. The specification includes:

- User stories for creating, viewing, updating, and deleting tasks
- Functional requirements focusing on authentication, authorization, task management, and data persistence
- Key entities (Task and User)
- Success criteria with measurable outcomes
- Edge cases for error handling

The specification was refined to be more technology-agnostic, removing specific implementation details like JWT, HTTP status codes, and specific frameworks from the requirements and success criteria. The specification is now ready for the planning phase.

## Outcome

Successfully created a feature specification document that follows the template structure and captures all essential requirements from the user's description. The specification is technology-agnostic where appropriate while maintaining all necessary functional requirements. A validation checklist was also created to ensure specification quality.

## Evaluation

The specification meets all acceptance criteria:
- Contains all mandatory sections (User Scenarios, Requirements, Success Criteria)
- Uses appropriate priority levels for user stories
- Includes acceptance scenarios for each user story
- Defines functional requirements that are testable
- Specifies measurable success criteria
- Identifies key entities and edge cases
- Maintains technology-agnostic language in requirements and success criteria