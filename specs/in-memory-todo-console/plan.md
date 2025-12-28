# Implementation Plan: In-Memory Todo Console Application (Phase I)

**Feature**: In-Memory Todo Console Application (Phase I)
**Feature Branch**: `001-in-memory-todo-console`
**Created**: 2025-12-25
**Status**: Draft
**Author**: Claude Code

## Technical Context

**Programming Language**: Python 3.13+
**Project Management**: uv for dependency management and project setup
**Architecture**: Console application with layered architecture (CLI, Domain, Application Flow)
**Data Storage**: In-memory collection with 24-hour expiration
**Task ID Generation**: Integer auto-increment starting from 1
**CLI Interaction**: Command-line arguments approach
**Error Handling**: Return error messages and continue processing
**Import/Export**: JSON format support

### Dependencies
- Python 3.13+ (required by project constraints)
- uv (for project management)
- Standard library only (no external dependencies for Phase I)

### Unknowns
- None identified (all clarifications resolved in specification)

## Constitution Check

This implementation plan aligns with the project constitution:

### Modularity
- Clear separation of concerns between CLI layer, domain layer, and application flow
- Each component will have well-defined interfaces and minimal coupling

### Reliability
- Graceful error handling with controlled error messages
- Deterministic behavior with same input producing same output

### Reproducibility
- Project setup using uv with documented dependencies
- Consistent environment setup through uv

### Spec-Driven Development
- Implementation follows the approved specification
- All functionality traceable to functional requirements in spec

### Security
- No authentication required for Phase I (will be added in later phases)
- In-memory storage reduces data persistence security concerns for this phase

## Phase 0: Research & Analysis

### Research Findings
- **Task Storage Decision**: Dict keyed by task ID provides O(1) lookup performance compared to O(n) for list iteration. For CLI applications where users may have many tasks, this provides better performance for operations like update, delete, and toggle completion.
- **ID Generation**: Integer auto-increment is simpler and more human-readable than UUIDs, which is important for CLI applications where users need to reference task IDs directly.
- **State Management**: Encapsulated task manager class provides better testability and clarity compared to global state, supporting modularity principle.
- **CLI Framework**: Using Python's built-in argparse module for command-line argument parsing, as it's part of the standard library and meets the requirements without adding external dependencies.

## Phase 1: Design & Contracts

### Data Model (data-model.md)

#### Task Entity
- **id**: integer (auto-increment starting from 1)
- **title**: string (required, max 200 characters)
- **description**: string | null (optional, max 1000 characters)
- **completed**: boolean (default: false)
- **created_at**: datetime (for expiration tracking)
- **last_accessed**: datetime (for expiration tracking)

#### TaskList Entity
- **tasks**: dict (key: task_id, value: Task object)
- **next_id**: integer (next auto-increment ID)
- **expiration_hours**: integer (default: 24)

### API Contracts

#### CLI Commands
- `todo add "Task Title" ["Description"]` - Add a new task
- `todo list` - List all tasks
- `todo update <id> ["New Title"] ["New Description"]` - Update task details
- `todo complete <id>` - Mark task as complete
- `todo uncomplete <id>` - Mark task as pending
- `todo delete <id>` - Delete a task
- `todo export` - Export tasks to JSON
- `todo import <file>` - Import tasks from JSON file

#### Return Codes
- 0: Success
- 1: General error
- 2: Invalid arguments

### Quickstart Guide

1. **Setup**: Install uv, then run `uv sync` to install dependencies
2. **Run**: Execute `python -m todo.main` or create a console script
3. **Usage**: Use command-line arguments as specified above

## Phase 2: Implementation Tasks

### Task 1: Project Setup
- Create project structure using uv
- Set up Python 3.13+ environment
- Configure basic project files (pyproject.toml, etc.)

### Task 2: Define Task Data Model
- Create Task class with required attributes
- Implement validation for title (non-empty, max 200 chars) and description (max 1000 chars)

### Task 3: Implement Task Manager
- Create TaskManager class with in-memory storage (dict)
- Implement auto-increment ID generation
- Add methods for CRUD operations
- Implement task expiration (24 hours)

### Task 4: Implement CLI Layer
- Use argparse for command-line argument parsing
- Create command handlers for each operation
- Implement error handling that continues processing

### Task 5: Add Import/Export Functionality
- Implement JSON import/export for tasks
- Validate imported data format

### Task 6: Testing and Validation
- Test all acceptance scenarios from specification
- Validate error handling
- Verify deterministic behavior

## Risk Analysis

### High Risk Items
- **Memory Management**: With 24-hour expiration, ensure proper cleanup to prevent memory leaks
- **Data Validation**: Ensure all input validation is properly implemented to prevent errors

### Mitigation Strategies
- Implement proper cleanup in TaskManager for expired tasks
- Add comprehensive input validation at the CLI and domain layers

## Quality Gates

- All functional requirements (FR-001 through FR-014) implemented
- All acceptance scenarios validated
- Deterministic behavior verified
- Error handling tested with invalid inputs
- Code follows separation of concerns
- No global mutable state