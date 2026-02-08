# Data Model: AI Agent based Todo Application

**Feature**: 001-ai-agent-todo
**Date**: 2026-01-04
**Status**: Design

## Task Entity

### Core Attributes
- **task_id**: `string | number` (Primary Key, Unique, Persistent)
  - Globally unique identifier for each task
  - Remains constant throughout task lifecycle
  - Used for all operations (edit, delete, complete)

- **title**: `string` (Required, Max 255 characters)
  - Task title/description
  - Required field for all tasks
  - Can be updated during edit operations

- **description**: `string | null` (Optional, Max 1000 characters)
  - Detailed task description
  - Optional field that can be null
  - Can be updated during edit operations

- **completed**: `boolean` (Required, Default: false)
  - Task completion status
  - Boolean value representing completion state
  - Toggled between true/false during completion operations

- **created_at**: `timestamp` (Required, Auto-generated)
  - Timestamp of task creation
  - Set automatically when task is created
  - Cannot be modified after creation

- **updated_at**: `timestamp` (Required, Auto-generated)
  - Timestamp of last task update
  - Updated automatically on any modification
  - Used for tracking task changes

### Validation Rules
- `task_id`: Must be unique across all tasks, non-empty
- `title`: Required, minimum 1 character, maximum 255 characters
- `completed`: Must be boolean value (true/false)
- `created_at`: Must be valid timestamp, set only at creation
- `updated_at`: Must be valid timestamp, updated on every modification

## State Management Model

### Task State Object
```typescript
interface TaskState {
  tasks: Task[];
  selectedTaskId: string | null;
  isLoading: boolean;
  error: string | null;
}
```

### State Transitions

#### Creation
- `task_id` assigned (new unique identifier)
- `title` set from user input
- `description` set from user input (or null)
- `completed` set to false
- `created_at` set to current timestamp
- `updated_at` set to current timestamp

#### Edit/Update
- `title` updated from user input
- `description` updated from user input
- `updated_at` updated to current timestamp
- `task_id` remains unchanged

#### Completion Toggle
- `completed` toggled (true ↔ false)
- `updated_at` updated to current timestamp
- Other attributes remain unchanged

#### Deletion
- Task removed from state
- Task removed from persistence layer
- `task_id` becomes invalid for future operations

## API Contract Model

### Task Request/Response Schemas

#### Create Task Request
```json
{
  "title": "string (required)",
  "description": "string (optional)",
  "completed": "boolean (default: false)"
}
```

#### Update Task Request
```json
{
  "title": "string (optional)",
  "description": "string (optional)"
}
```

#### Toggle Completion Request
```json
{
  "completed": "boolean (required)"
}
```

#### Task Response
```json
{
  "task_id": "string (required)",
  "title": "string (required)",
  "description": "string (optional)",
  "completed": "boolean (required)",
  "created_at": "timestamp (required)",
  "updated_at": "timestamp (required)"
}
```

## AI Intent Mapping Model

### Intent Types
- **EDIT_TASK**: Update existing task content
  - Parameters: `task_id`, `title?`, `description?`
  - Validation: Task with `task_id` must exist

- **DELETE_TASK**: Remove existing task
  - Parameters: `task_id`
  - Validation: Task with `task_id` must exist

- **COMPLETE_TASK**: Mark task as completed
  - Parameters: `task_id`
  - Validation: Task with `task_id` must exist

- **UNCOMPLETE_TASK**: Mark task as incomplete
  - Parameters: `task_id`
  - Validation: Task with `task_id` must exist

- **CREATE_TASK**: Create new task
  - Parameters: `title`, `description?`
  - Validation: Title must be provided

## Relationships

### User-Task Relationship
- Each task belongs to a single user
- User can have multiple tasks
- Tasks are isolated between users
- Foreign key relationship: `user_id` → `user.id`

### Task Dependencies
- No complex dependencies between tasks
- Each task is independent
- Operations on one task do not affect others
- State changes are isolated to individual tasks

## Constraints and Rules

### Data Integrity
- Task IDs must remain unique throughout application lifecycle
- Completed status must be a boolean value
- Timestamps must be valid date/time values
- Required fields cannot be null when creating tasks

### Business Rules
- Users can only modify their own tasks
- Deleted tasks cannot be operated on
- Task creation must have a valid title
- Task updates cannot create duplicate identifiers