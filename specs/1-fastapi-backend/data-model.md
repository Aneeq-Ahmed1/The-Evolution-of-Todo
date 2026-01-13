# Data Model: FastAPI Backend for Todo Application

**Feature**: 1-fastapi-backend
**Date**: 2026-01-05

## Entity: Task

**Description**: Represents a user's todo item that can be created, read, updated, and deleted.

**Fields**:
- `id`: Integer (Primary Key)
  - Auto-incrementing identifier for the task
  - Required for database indexing and API access
- `user_id`: String (Indexed)
  - Foreign key reference to the user who owns the task
  - Extracted from JWT token during creation
  - Required for user isolation
- `title`: String (1-200 characters)
  - Required title of the task
  - Must be validated to be between 1-200 characters
- `description`: Optional[String] (Max 1000 characters)
  - Optional detailed description of the task
  - Can be null/empty
  - If provided, must be max 1000 characters
- `completed`: Boolean
  - Status of whether the task is completed
  - Default value: False
- `created_at`: DateTime
  - Timestamp of when the task was created
  - Auto-populated on creation
- `updated_at`: DateTime
  - Timestamp of when the task was last updated
  - Auto-updated on modifications

**Validation Rules**:
- Title length: 1-200 characters (inclusive)
- Description length: 0-1000 characters (if provided)
- User_id must match the authenticated user from JWT
- All tasks must belong to exactly one user
- Queries must always filter by user_id

**Relationships**:
- Belongs to: User (identified by user_id from JWT)

## Entity: User (Conceptual)

**Description**: Represents a user in the system. Note: The user data is managed by Better Auth on the frontend, but user_id is extracted from JWT tokens for task ownership.

**Fields**:
- `user_id`: String
  - Unique identifier extracted from JWT token
  - Used to associate tasks with users
- `email`: String (from JWT)
  - Email address extracted from JWT token
  - Used for identification purposes

**Constraints**:
- Same email must not be allowed to register twice (though this is handled by Better Auth frontend)
- User isolation: Tasks can only be accessed by their owner

## Database Schema Considerations

**Indexing**:
- Primary key: id (auto-indexed)
- Secondary index: user_id (for efficient user-based queries)
- Potential composite index: (user_id, completed) for filtered queries

**Constraints**:
- NOT NULL constraints on required fields (id, user_id, title)
- Check constraint on title length (1-200)
- Check constraint on description length (0-1000 when present)
- Default value for completed field (False)
- Automatic timestamp population for created_at and updated_at

## State Transitions

**Task Completion**:
- `completed = False` → `completed = True` (via PATCH /complete endpoint)
- `completed = True` → `completed = False` (via PATCH /complete endpoint)

**Task Modification**:
- Creation: New task with completed = False (default)
- Update: Any field except user_id and id can be modified
- Deletion: Task is removed from database (with proper authorization)