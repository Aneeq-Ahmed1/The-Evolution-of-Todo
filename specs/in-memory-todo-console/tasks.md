# Tasks: In-Memory Todo Console Application (Phase I)

**Feature**: In-Memory Todo Console Application (Phase I)
**Feature Branch**: `001-in-memory-todo-console`
**Created**: 2025-12-25
**Status**: Draft

## Implementation Strategy

This implementation will follow an incremental delivery approach:
- MVP: User Story 1 (Add Tasks) with minimal viable functionality
- Incremental: Add other user stories in priority order (P1, P2, P3...)
- Each user story will be independently testable and deliverable

## Phase 1: Project Setup

- [ ] T001 Create project structure using uv in `todo/` directory
- [ ] T002 Configure pyproject.toml with Python 3.13+ requirement and project metadata
- [ ] T003 Set up basic directory structure (`src/todo/`, `tests/`, `docs/`)
- [ ] T004 Create main application entry point in `src/todo/main.py`
- [ ] T005 Initialize git repository with proper .gitignore for Python/uv

## Phase 2: Foundational Components

- [ ] T010 Define Task data model class in `src/todo/models.py` with all required attributes
- [ ] T011 Implement Task validation methods for title and description in `src/todo/models.py`
- [ ] T012 Create TaskManager class in `src/todo/manager.py` with in-memory storage
- [ ] T013 Implement auto-increment ID generation in TaskManager
- [ ] T014 Add task expiration functionality (24-hour cleanup) to TaskManager
- [ ] T015 Set up command-line argument parsing using argparse in main.py

## Phase 3: User Story 1 - Add New Tasks (Priority: P1)

**Goal**: Enable users to add tasks to their todo list with required title and optional description

**Independent Test**: Can be fully tested by running the CLI command to add a task and verifying it appears in the task list, delivering the core value of task management.

**Acceptance Scenarios**:
1. Given an empty todo list, When I add a task with a valid title, Then the task is created with a unique integer ID starting from 1 and status 'pending'
2. Given a task with a valid title, When I add it to the list, Then it appears in the task list with title, ID, and status

- [ ] T020 [US1] Implement add_task method in TaskManager with validation
- [ ] T021 [US1] Create CLI handler for 'add' command in main.py
- [ ] T022 [US1] Add input validation for title (non-empty, max 200 chars) and description (max 1000 chars)
- [ ] T023 [US1] Ensure new tasks get unique integer IDs starting from 1 with 'pending' status
- [ ] T024 [US1] Test add functionality with valid inputs
- [ ] T025 [US1] Test add functionality with invalid inputs (empty title, too long title/description)

## Phase 4: User Story 2 - View All Tasks (Priority: P1)

**Goal**: Enable users to view all their tasks showing ID, title, and completion status

**Independent Test**: Can be fully tested by adding tasks and then viewing the complete list, delivering visibility into all tasks.

**Acceptance Scenarios**:
1. Given I have multiple tasks in the system, When I request to view all tasks, Then all tasks are displayed with their ID, title, and completion status
2. Given I have no tasks in the system, When I request to view all tasks, Then an empty list is displayed

- [ ] T030 [US2] Implement list_tasks method in TaskManager to return all tasks
- [ ] T031 [US2] Create CLI handler for 'list' command in main.py
- [ ] T032 [US2] Format task display with ID, title, and status
- [ ] T033 [US2] Handle empty task list case with appropriate message
- [ ] T034 [US2] Test list functionality with multiple tasks
- [ ] T035 [US2] Test list functionality with empty task list

## Phase 5: User Story 3 - Mark Tasks Complete (Priority: P2)

**Goal**: Enable users to mark tasks as complete to track their progress

**Independent Test**: Can be fully tested by adding a task and then marking it complete, delivering the complete task lifecycle.

**Acceptance Scenarios**:
1. Given I have a pending task, When I mark it as complete, Then its status changes to 'completed'
2. Given I have a completed task, When I mark it again, Then it remains completed (idempotent operation)

- [ ] T040 [US3] Implement toggle_completion method in TaskManager
- [ ] T041 [US3] Create CLI handler for 'complete' command in main.py
- [ ] T042 [US3] Create CLI handler for 'uncomplete' command in main.py
- [ ] T043 [US3] Ensure idempotent behavior for completion operations
- [ ] T044 [US3] Test completion of pending tasks
- [ ] T045 [US3] Test idempotent behavior with already completed tasks

## Phase 6: User Story 4 - Update Task Details (Priority: P3)

**Goal**: Enable users to update their task details to refine their todo items

**Independent Test**: Can be fully tested by adding a task and then updating its details, delivering the ability to maintain accurate task information.

**Acceptance Scenarios**:
1. Given I have an existing task, When I update its title, Then the title is changed while preserving the ID
2. Given I have an existing task, When I update its description, Then the description is changed while preserving other attributes

- [ ] T050 [US4] Implement update_task method in TaskManager with validation
- [ ] T051 [US4] Create CLI handler for 'update' command in main.py
- [ ] T052 [US4] Add validation for updated title and description
- [ ] T053 [US4] Preserve task ID during updates
- [ ] T054 [US4] Test updating task title while preserving ID
- [ ] T055 [US4] Test updating task description while preserving other attributes

## Phase 7: User Story 5 - Delete Tasks (Priority: P3)

**Goal**: Enable users to delete tasks to remove items they no longer need to track

**Independent Test**: Can be fully tested by adding a task and then deleting it, delivering the ability to manage the task list size.

**Acceptance Scenarios**:
1. Given I have an existing task, When I delete it, Then it is removed from the task list permanently
2. Given I attempt to delete a non-existent task, When I run the delete command, Then an appropriate error is returned

- [ ] T060 [US5] Implement delete_task method in TaskManager
- [ ] T061 [US5] Create CLI handler for 'delete' command in main.py
- [ ] T062 [US5] Handle invalid task ID with appropriate error message
- [ ] T063 [US5] Test deletion of existing tasks
- [ ] T064 [US5] Test error handling for non-existent task IDs

## Phase 8: Import/Export Functionality

- [ ] T070 Implement JSON export functionality in TaskManager
- [ ] T071 Create CLI handler for 'export' command in main.py
- [ ] T072 Implement JSON import functionality in TaskManager
- [ ] T073 Create CLI handler for 'import' command in main.py
- [ ] T074 Add validation for imported JSON data format
- [ ] T075 Test export functionality with multiple tasks
- [ ] T076 Test import functionality with valid JSON
- [ ] T077 Test import validation with invalid JSON

## Phase 9: Error Handling & Edge Cases

- [ ] T080 Implement controlled error handling for invalid task IDs across all operations
- [ ] T081 Add error handling for empty title when adding/updating tasks
- [ ] T082 Add error handling for title exceeding 200 characters
- [ ] T083 Add error handling for description exceeding 1000 characters
- [ ] T084 Ensure error messages are returned and processing continues (fail-soft approach)
- [ ] T085 Test all error scenarios from specification

## Phase 10: Polish & Cross-Cutting Concerns

- [ ] T090 Implement proper datetime handling for task expiration tracking
- [ ] T091 Add comprehensive logging for debugging purposes
- [ ] T092 Write usage documentation and help messages
- [ ] T093 Implement graceful shutdown and cleanup
- [ ] T094 Run all acceptance scenarios from specification
- [ ] T095 Verify deterministic behavior with same input producing same output
- [ ] T096 Ensure separation of domain logic and CLI interaction layer
- [ ] T097 Test all functional requirements FR-001 through FR-014

## Dependencies

User stories dependency graph:
- US1 (Add Tasks) - Foundation, no dependencies
- US2 (View Tasks) - Depends on US1 for data
- US3 (Mark Complete) - Depends on US1 for data
- US4 (Update Tasks) - Depends on US1 for data
- US5 (Delete Tasks) - Depends on US1 for data

## Parallel Execution Examples

Tasks that can be developed in parallel:
- CLI command handlers (T021, T031, T041, T042, T051, T061) can be developed independently
- TaskManager methods (T020, T030, T040, T050, T060) can be developed in parallel
- Error handling tasks (T080-T084) can be implemented after core functionality