# Feature Specification: FastAPI Backend for Todo Application

**Feature Branch**: `1-fastapi-backend`
**Created**: 2026-01-05
**Status**: Draft
**Input**: User description: "Project Phase: Phase II – Full-Stack Web Application (Backend)

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
- If mismatch → 403 Forbidden

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
- Authorization: Bearer <token>
- Content-Type: application/json

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

End of specification."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create Todo Task (Priority: P1)

As a registered user, I want to create new todo tasks so that I can keep track of my responsibilities and goals.

**Why this priority**: This is the core functionality of a todo application - users must be able to create tasks to have value from the system.

**Independent Test**: Can be fully tested by creating a new task via the API endpoint and verifying it appears in the user's task list, delivering the fundamental value of task creation.

**Acceptance Scenarios**:

1. **Given** I am an authenticated user with a valid JWT token, **When** I make a POST request to `/api/{my_user_id}/tasks` with a valid title and optional description, **Then** a new task is created and returned with a 201 status code.
2. **Given** I am an unauthenticated user or have an invalid JWT token, **When** I make a POST request to `/api/{user_id}/tasks`, **Then** I receive a 401 Unauthorized response.

---

### User Story 2 - View My Todo Tasks (Priority: P1)

As a registered user, I want to view my todo tasks so that I can see what I need to do and track my progress.

**Why this priority**: This is fundamental to the user experience - users need to see their tasks to manage them effectively.

**Independent Test**: Can be fully tested by creating tasks and then retrieving them via the API endpoint, delivering the core value of task visibility.

**Acceptance Scenarios**:

1. **Given** I am an authenticated user with existing tasks, **When** I make a GET request to `/api/{my_user_id}/tasks`, **Then** I receive a list of my tasks filtered by my user_id.
2. **Given** I am an authenticated user filtering by status, **When** I make a GET request to `/api/{my_user_id}/tasks?status=completed`, **Then** I receive only my completed tasks.

---

### User Story 3 - Update and Complete My Tasks (Priority: P2)

As a registered user, I want to update and mark my tasks as completed so that I can track my progress and modify task details as needed.

**Why this priority**: Allows users to manage their tasks beyond just creation, which is essential for a functional todo system.

**Independent Test**: Can be fully tested by updating task details or toggling completion status via API endpoints, delivering the value of task management.

**Acceptance Scenarios**:

1. **Given** I am an authenticated user with an existing task, **When** I make a PUT request to `/api/{my_user_id}/tasks/{task_id}` with updated details, **Then** the task is updated and returned.
2. **Given** I am an authenticated user with an existing task, **When** I make a PATCH request to `/api/{my_user_id}/tasks/{task_id}/complete`, **Then** the task's completion status is toggled.

---

### User Story 4 - Delete My Tasks (Priority: P3)

As a registered user, I want to delete tasks I no longer need so that I can keep my todo list clean and organized.

**Why this priority**: Provides users with the ability to remove tasks that are no longer relevant, completing the CRUD cycle.

**Independent Test**: Can be fully tested by deleting a task via the API endpoint, delivering the value of task removal.

**Acceptance Scenarios**:

1. **Given** I am an authenticated user with an existing task, **When** I make a DELETE request to `/api/{my_user_id}/tasks/{task_id}`, **Then** the task is deleted and no longer appears in my task list.

---

### Edge Cases

- What happens when a user tries to access another user's tasks? The system should return a 403 Forbidden error.
- How does the system handle expired JWT tokens? The system should return a 401 Unauthorized error.
- What happens when a user tries to access a non-existent task? The system should return a 404 Not Found error.
- How does the system handle requests with invalid request body formats? The system should return a 422 Validation Error.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST authenticate users using secure tokens from request headers
- **FR-002**: System MUST verify that requesting user has permission to access requested resources
- **FR-003**: System MUST only return tasks that belong to the authenticated user
- **FR-004**: System MUST store tasks with user identifier, title, description, completion status, and timestamps
- **FR-005**: System MUST provide operations to create, read, update, and delete tasks
- **FR-006**: System MUST support filtering tasks by completion status (all, completed, pending)
- **FR-007**: System MUST validate that task titles are between 1-200 characters
- **FR-008**: System MUST validate that task descriptions are max 1000 characters if provided
- **FR-009**: System MUST return appropriate status responses for all operations
- **FR-010**: System MUST handle expired authentication tokens appropriately
- **FR-011**: System MUST reject requests without valid authentication
- **FR-012**: System MUST ensure tasks cannot be accessed by users other than the owner
- **FR-013**: System MUST support toggling task completion status
- **FR-014**: System MUST store task creation and update timestamps automatically
- **FR-015**: System MUST persist data using a reliable database system

### Key Entities *(include if feature involves data)*

- **Task**: Represents a user's todo item with properties including id, user_id, title, description, completion status, and timestamps
- **User**: Identified by user_id extracted from JWT token, owns multiple tasks

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Backend service is successfully deployed and accessible for API requests
- **SC-002**: All endpoints require valid authentication with 99% success rate for authorized requests
- **SC-003**: Tasks are properly isolated by user with 100% accuracy in preventing cross-user access
- **SC-004**: System handles concurrent requests from multiple users without data leakage between users
- **SC-005**: All create, read, update, and delete operations complete successfully with appropriate responses
- **SC-006**: Authentication validation completes within 100ms for 95% of requests
- **SC-007**: Service endpoints respond within 500ms for 95% of requests under normal load
- **SC-008**: Backend successfully integrates with existing frontend with no compatibility issues