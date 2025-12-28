# Feature Specification: Full-Stack Todo Web Application

**Feature Branch**: `1-full-stack-todo`
**Created**: 2025-12-28
**Status**: Draft
**Input**: User description: "# Phase II – Full-Stack Todo Web Application

## Phase Objective
Evolve the Phase I console-based Todo system into a production-grade, multi-user full-stack web application with persistent storage and secure authentication, implemented strictly via Spec-Kit Plus and Claude Code.

---

## Context:
Phase I delivered a working in-memory Python console Todo application.
This phase transforms it into a modern, multi-user, full-stack web application.

---
## Scope (Phase II Only)

- Multi-user system
- Persistent data storage (PostgreSQL)
- RESTful backend API
- Web-based frontend UI
- JWT-based authentication
- No AI chatbot interaction in this phase

---

## Functional Requirements

### FR-1: User Authentication
- Users can sign up and sign in
- Authentication handled via Better Auth (frontend)
- JWT tokens issued on login
- All backend requests require valid JWT

### FR-2: Task Ownership
- Each task is associated with exactly one user
- Users can only access their own tasks
- Task ownership enforced on every API operation

### FR-3: Create Task
- Authenticated users can create tasks
- Fields:
  - title (required, max 200 chars)
  - description (optional, max 1000 chars)
- Default status: pending
- Task persisted in database

### FR-4: View Tasks
- Users can retrieve all their tasks
- Support basic filtering:
  - status (pending/completed)
- Tasks returned only for authenticated user

### FR-5: Update Task
- Users can update title and description
- Task must belong to authenticated user
- Invalid access returns 403 Forbidden

### FR-6: Delete Task
- Users can delete their own tasks
- Tasks are soft-deleted (marked as deleted but retained in DB)
- Unauthorized access blocked

### FR-7: Mark Task Complete
- Users can toggle completion state
- Operation is idempotent

---

## Non-Functional Requirements

- Stateless backend services
- Deterministic API behavior
- Clear API error responses (401, 403, 404)
- Responsive frontend UI
- Separation of frontend and backend concerns

---

## Data Model (Logical)

User:
- id: string
- email: string
- created_at: timestamp

Task:
- id: integer
- user_id: string (foreign key)
- title: string
- description: string | null
- completed: boolean
- created_at: timestamp
- updated_at: timestamp

---

## Constraints

- Frontend: Next.js (App Router)
- Backend: FastAPI (Python)
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth + JWT
- API secured via Authorization: Bearer token
- Dependency & execution managed via `uv`
- No manual code writing
- Must comply with `/sp.constitution`

---

## Acceptance Criteria

- Users cannot access other users' tasks
- All CRUD operations persist correctly
- Unauthorized requests return 401
- Forbidden access returns 403
- Frontend and backend integrate cleanly
- API behavior traceable to spec

---

## Requirements:
- Implement all 5 basic Todo features:
  Add, View, Update, Delete, Mark Complete
- Multi-user system: each user sees only their own tasks
- Persistent storage using Neon Serverless PostgreSQL
- RESTful API built with FastAPI and SQLModel
- Responsive frontend built with Next.js (App Router)
- Authentication using Better Auth on frontend
- JWT-based authentication between frontend and backend
- All API routes secured and filtered by authenticated user

---

##Architecture:
- Monorepo structure with /frontend and /backend
- Specs stored under /specs using Spec-Kit conventions
- Shared JWT secret via environment variables

---

## Out of Scope (Explicit)

- AI chatbot
- MCP tools
- Kubernetes deployment
- Kafka / Dapr
- Advanced filtering or sorting

---

## Phase Completion Definition

Phase II is complete when:
- Full-stack app runs locally
- Authentication and authorization enforced
- Tasks persist across sessions
- Ready for Phase III chatbot integration"

## Clarifications *(optional)*

### Session 2025-12-28

- Q: What should happen when a user deletes a task? → A: Tasks should be soft-deleted (marked as deleted but retained in DB)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create and Manage Personal Tasks (Priority: P1)

A registered user wants to create, view, update, and delete their personal tasks through a web interface. They can sign up for an account, log in, create tasks with titles and descriptions, mark tasks as complete, and manage their task list.

**Why this priority**: This represents the core functionality of the todo application and delivers immediate value to users by allowing them to manage their tasks in a persistent way.

**Independent Test**: Can be fully tested by creating a user account, adding tasks, viewing them, updating them, and deleting them. The system persists tasks across sessions and ensures only the owner can access their tasks.

**Acceptance Scenarios**:

1. **Given** a user is registered and logged in, **When** they create a new task with a title and description, **Then** the task is saved to their account and appears in their task list
2. **Given** a user has tasks in their account, **When** they mark a task as complete, **Then** the task status updates and reflects as completed in their task list
3. **Given** a user has tasks in their account, **When** they update a task title or description, **Then** the changes are saved and reflected in their task list
4. **Given** a user has tasks in their account, **When** they delete a task, **Then** the task is soft-deleted (marked as deleted but still retained in the system)

---

### User Story 2 - User Authentication and Authorization (Priority: P1)

A user wants to securely sign up for an account, log in, and have their tasks protected so that other users cannot access their personal tasks. The system must ensure that users can only access their own data.

**Why this priority**: Security and data isolation are fundamental requirements for a multi-user system. Without proper authentication and authorization, the entire application is compromised.

**Independent Test**: Can be fully tested by creating multiple user accounts, having each user create tasks, and verifying that users cannot access tasks belonging to other users.

**Acceptance Scenarios**:

1. **Given** a user is not registered, **When** they sign up with valid credentials, **Then** an account is created and they can log in
2. **Given** a user has an account, **When** they log in with correct credentials, **Then** they receive a valid JWT token and can access the application
3. **Given** a user is logged in, **When** they try to access another user's tasks, **Then** the system returns a 403 Forbidden error

---

### User Story 3 - View and Filter Tasks (Priority: P2)

A user wants to view all their tasks in one place and filter them by status (pending/completed) to better organize their workflow. They can see a clean, responsive interface that works well on different devices.

**Why this priority**: This enhances the user experience by providing better organization and visibility of tasks, making the application more useful for daily use.

**Independent Test**: Can be fully tested by creating multiple tasks with different statuses, then using the filtering functionality to display only pending or completed tasks.

**Acceptance Scenarios**:

1. **Given** a user has multiple tasks with different statuses, **When** they view their task list, **Then** all their tasks are displayed in a responsive interface
2. **Given** a user has both pending and completed tasks, **When** they filter by "completed" status, **Then** only completed tasks are shown
3. **Given** a user has both pending and completed tasks, **When** they filter by "pending" status, **Then** only pending tasks are shown

---

### Edge Cases

- What happens when a user tries to create a task with an empty title?
- How does the system handle JWT token expiration during a session?
- What happens when a user tries to access the application without authentication?
- How does the system handle database connection failures?
- What happens when a user attempts to update a task that doesn't exist?
- How does the system handle very large task descriptions (at the 1000 character limit)?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to sign up with an email and password
- **FR-002**: System MUST allow users to sign in with their credentials and receive a JWT token
- **FR-003**: System MUST authenticate all API requests using JWT tokens in Authorization header
- **FR-004**: System MUST allow authenticated users to create tasks with title (max 200 chars) and description (max 1000 chars)
- **FR-005**: System MUST associate each task with the user who created it
- **FR-006**: System MUST allow users to retrieve only their own tasks
- **FR-007**: System MUST allow users to update their own task titles and descriptions
- **FR-008**: System MUST allow users to soft-delete their own tasks (mark as deleted but retain in DB)
- **FR-009**: System MUST allow users to toggle task completion status (idempotent operation)
- **FR-010**: System MUST provide basic filtering by task status (pending/completed)
- **FR-011**: System MUST return appropriate HTTP error codes (401 for unauthorized, 403 for forbidden, 404 for not found)
- **FR-012**: System MUST persist all user data in PostgreSQL database
- **FR-013**: System MUST enforce data validation on task creation (title required, character limits)
- **FR-014**: System MUST ensure users cannot access other users' tasks
- **FR-015**: Frontend MUST provide a responsive web interface for task management

### Key Entities *(include if feature involves data)*

- **User**: Represents a registered user with authentication credentials; has many Tasks; attributes include id (string), email (string), created_at (timestamp)
- **Task**: Represents a user's task item; belongs to one User; attributes include id (integer), user_id (string), title (string), description (string or null), completed (boolean), deleted (boolean), created_at (timestamp), updated_at (timestamp)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete account registration and login within 2 minutes
- **SC-002**: Users can create, view, update, and delete tasks with response times under 2 seconds
- **SC-003**: 100% of users can only access their own tasks (no cross-user data access)
- **SC-004**: System maintains task data persistence across application restarts
- **SC-005**: Frontend UI is responsive and usable on desktop, tablet, and mobile devices
- **SC-006**: All authenticated API requests successfully validate JWT tokens
- **SC-007**: System properly returns 401/403 errors for unauthorized/forbidden access attempts
- **SC-008**: 95% of users can successfully complete the primary task management workflow (create, update, mark complete, delete)