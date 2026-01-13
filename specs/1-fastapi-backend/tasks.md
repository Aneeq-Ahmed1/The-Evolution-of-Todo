---
description: "Task list for FastAPI Backend implementation"
---

# Tasks: FastAPI Backend for Todo Application

**Input**: Design documents from `/specs/1-fastapi-backend/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create backend directory structure per implementation plan
- [X] T002 Initialize Python project with FastAPI, SQLModel, PyJWT dependencies using uv
- [X] T003 [P] Create pyproject.toml with all required dependencies
- [X] T004 [P] Create backend/CLAUDE.md with backend development guidelines

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Setup database connection framework in backend/db.py
- [X] T006 [P] Implement JWT authentication/authorization framework in backend/auth.py
- [X] T007 [P] Create environment configuration management in backend/settings.py
- [X] T008 Create base Task model in backend/models.py
- [X] T009 Create Pydantic request/response schemas in backend/schemas.py
- [X] T010 Setup FastAPI app entry point in backend/main.py
- [X] T011 Configure error handling and consistent error response format

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create Todo Task (Priority: P1) 🎯 MVP

**Goal**: Enable authenticated users to create new todo tasks via POST /api/{user_id}/tasks endpoint

**Independent Test**: Can be fully tested by creating a new task via the API endpoint and verifying it appears in the user's task list, delivering the fundamental value of task creation.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T012 [P] [US1] Contract test for POST /api/{user_id}/tasks endpoint in tests/contract/test_tasks_create.py
- [ ] T013 [P] [US1] Integration test for task creation journey in tests/integration/test_task_creation.py

### Implementation for User Story 1

- [X] T014 [P] [US1] Create TaskCreate schema in backend/schemas.py
- [X] T015 [P] [US1] Create TaskRead schema in backend/schemas.py
- [X] T016 [US1] Implement Task service methods for creation in backend/services/task_service.py
- [X] T017 [US1] Implement POST /api/{user_id}/tasks endpoint in backend/routes/tasks.py
- [X] T018 [US1] Add input validation for title and description length in backend/schemas.py
- [X] T019 [US1] Add JWT verification and user_id matching validation to create endpoint

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View My Todo Tasks (Priority: P1)

**Goal**: Enable authenticated users to view their todo tasks via GET /api/{user_id}/tasks endpoint with optional status filtering

**Independent Test**: Can be fully tested by creating tasks and then retrieving them via the API endpoint, delivering the core value of task visibility.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T020 [P] [US2] Contract test for GET /api/{user_id}/tasks endpoint in tests/contract/test_tasks_list.py
- [ ] T021 [P] [US2] Integration test for task listing journey in tests/integration/test_task_listing.py

### Implementation for User Story 2

- [X] T022 [P] [US2] Create TaskListResponse schema in backend/schemas.py
- [X] T023 [US2] Implement Task service methods for listing in backend/services/task_service.py
- [X] T024 [US2] Implement GET /api/{user_id}/tasks endpoint in backend/routes/tasks.py
- [X] T025 [US2] Add query parameter validation for status filtering in backend/schemas.py
- [X] T026 [US2] Add JWT verification and user_id matching validation to list endpoint
- [X] T027 [US2] Add proper filtering by user_id and status to task listing

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update and Complete My Tasks (Priority: P2)

**Goal**: Enable authenticated users to update task details and toggle completion status via PUT and PATCH endpoints

**Independent Test**: Can be fully tested by updating task details or toggling completion status via API endpoints, delivering the value of task management.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T028 [P] [US3] Contract test for PUT /api/{user_id}/tasks/{id} endpoint in tests/contract/test_tasks_update.py
- [ ] T029 [P] [US3] Contract test for PATCH /api/{user_id}/tasks/{id}/complete endpoint in tests/contract/test_tasks_complete.py
- [ ] T030 [P] [US3] Integration test for task update and completion journey in tests/integration/test_task_management.py

### Implementation for User Story 3

- [X] T031 [P] [US3] Create TaskUpdate schema in backend/schemas.py
- [X] T032 [P] [US3] Create TaskToggleComplete schema in backend/schemas.py
- [X] T033 [US3] Implement Task service methods for update in backend/services/task_service.py
- [X] T034 [US3] Implement Task service methods for toggle completion in backend/services/task_service.py
- [X] T035 [US3] Implement PUT /api/{user_id}/tasks/{id} endpoint in backend/routes/tasks.py
- [X] T036 [US3] Implement PATCH /api/{user_id}/tasks/{id}/complete endpoint in backend/routes/tasks.py
- [X] T037 [US3] Add JWT verification and user_id matching validation to update endpoints
- [X] T038 [US3] Add proper ownership verification for update and completion endpoints

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Delete My Tasks (Priority: P3)

**Goal**: Enable authenticated users to delete tasks they no longer need via DELETE /api/{user_id}/tasks/{id} endpoint

**Independent Test**: Can be fully tested by deleting a task via the API endpoint, delivering the value of task removal.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T039 [P] [US4] Contract test for DELETE /api/{user_id}/tasks/{id} endpoint in tests/contract/test_tasks_delete.py
- [ ] T040 [P] [US4] Integration test for task deletion journey in tests/integration/test_task_deletion.py

### Implementation for User Story 4

- [X] T041 [US4] Implement Task service methods for deletion in backend/services/task_service.py
- [X] T042 [US4] Implement DELETE /api/{user_id}/tasks/{id} endpoint in backend/routes/tasks.py
- [X] T043 [US4] Add JWT verification and user_id matching validation to delete endpoint
- [X] T044 [US4] Add proper ownership verification for delete endpoint

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T045 [P] Documentation updates in backend/README.md
- [X] T046 Add comprehensive error handling for all endpoints
- [X] T047 [P] Add API documentation with OpenAPI/Swagger
- [X] T048 [P] Add logging for all user operations in backend/main.py
- [X] T049 Security hardening and validation of all user inputs
- [X] T050 Run quickstart.md validation to ensure all functionality works

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P3)**: Can start after Foundational (Phase 2) - May integrate with other stories but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for POST /api/{user_id}/tasks endpoint in tests/contract/test_tasks_create.py"
Task: "Integration test for task creation journey in tests/integration/test_task_creation.py"

# Launch all schemas for User Story 1 together:
Task: "Create TaskCreate schema in backend/schemas.py"
Task: "Create TaskRead schema in backend/schemas.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence