# Data Model: AI Task Display Mapping

**Feature**: 001-ai-task-mapping
**Date**: 2026-01-04
**Status**: Design

## Display Mapping Entity

### Core Attributes
- **display_index**: `number` (Primary Key in mapping context, 1-based sequential)
  - Position of task in the displayed list
  - Sequential numbering starting from 1
  - Used for user-facing ordinal references

- **task_id**: `string | number` (Foreign Key, Internal identifier)
  - Internal unique identifier for the task
  - Maps to the actual task in the database
  - Used for backend operations

- **user_id**: `string | number` (Foreign Key, User identifier)
  - Links the mapping to the specific user session
  - Ensures mapping isolation between users
  - Required for multi-user support

- **created_at**: `timestamp` (Required, Auto-generated)
  - Timestamp when mapping was created
  - Used for tracking mapping freshness
  - Set automatically when mapping is created

- **updated_at**: `timestamp` (Required, Auto-generated)
  - Timestamp of last mapping update
  - Used for tracking mapping changes
  - Updated automatically on any modification

### Validation Rules
- `display_index`: Must be positive integer (≥ 1), unique within user session
- `task_id`: Must reference existing task in the system
- `user_id`: Must reference existing user in the system
- `created_at`: Must be valid timestamp, set only at creation
- `updated_at`: Must be valid timestamp, updated on every modification

## State Management Model

### Display Mapping State Object
```typescript
interface DisplayMappingState {
  mappings: Array<{
    display_index: number;
    task_id: string | number;
    user_id: string | number;
    created_at: Date;
    updated_at: Date;
  }>;
  user_id: string | number;
  last_updated: Date;
  isValid: boolean;
}
```

### State Transitions

#### Creation
- `display_index` assigned sequentially (1, 2, 3, ...)
- `task_id` set to internal task identifier
- `user_id` set to current user
- `created_at` set to current timestamp
- `updated_at` set to current timestamp

#### Update (on task list change)
- `display_index` reassigned based on new task order
- `task_id` remains unchanged for existing tasks
- `updated_at` updated to current timestamp
- Old mappings removed if task no longer exists

#### Deletion
- Mapping removed when corresponding task is deleted
- Remaining mappings reindexed to maintain sequential numbering
- `display_index` values updated to fill gaps

## Runtime Mapping Model

### Mapping Lifecycle

1. **Generation**: When task list is displayed, create mapping array
2. **Storage**: Store in user session context for AI agent access
3. **Validation**: Check mapping validity before use
4. **Refresh**: Update mapping when task list changes
5. **Cleanup**: Remove mapping when user session ends

### Mapping Operations

#### Generate Mapping
```typescript
function generateDisplayMapping(tasks: Task[], user_id: string): DisplayMapping[] {
  return tasks.map((task, index) => ({
    display_index: index + 1,  // 1-based indexing
    task_id: task.id,
    user_id: user_id,
    created_at: new Date(),
    updated_at: new Date()
  }));
}
```

#### Resolve Display Index
```typescript
function resolveDisplayIndex(display_index: number, user_id: string): string | null {
  const mapping = findMapping(display_index, user_id);
  return mapping ? mapping.task_id : null;
}
```

#### Update Mapping
```typescript
function updateDisplayMapping(new_tasks: Task[], user_id: string): void {
  const new_mapping = generateDisplayMapping(new_tasks, user_id);
  storeMapping(new_mapping, user_id);
}
```

## API Contract Model

### Mapping Request/Response Schemas

#### Get Task by Display Index Request
```json
{
  "display_index": "number (required)",
  "user_id": "string (required)"
}
```

#### Get Task by Display Index Response
```json
{
  "task_id": "string (required)",
  "display_index": "number (required)",
  "valid": "boolean (required)",
  "error": "string (optional)"
}
```

#### Refresh Mapping Request
```json
{
  "user_id": "string (required)",
  "tasks": [
    {
      "id": "string (required)",
      "title": "string (required)",
      "completed": "boolean (required)"
    }
  ]
}
```

#### Refresh Mapping Response
```json
{
  "mapping_updated": "boolean (required)",
  "total_mappings": "number (required)",
  "refreshed_at": "timestamp (required)"
}
```

## AI Intent Mapping Model

### Intent Types with Display Index
- **ORDINAL_COMPLETE_TASK**: Mark task as completed by display index
  - Parameters: `user_id`, `display_index`
  - Validation: Display index must exist in current mapping

- **ORDINAL_UNCOMPLETE_TASK**: Mark task as incomplete by display index
  - Parameters: `user_id`, `display_index`
  - Validation: Display index must exist in current mapping

- **ORDINAL_EDIT_TASK**: Edit task by display index
  - Parameters: `user_id`, `display_index`, `new_content?`
  - Validation: Display index must exist in current mapping

- **ORDINAL_DELETE_TASK**: Delete task by display index
  - Parameters: `user_id`, `display_index`
  - Validation: Display index must exist in current mapping

- **ORDINAL_GET_TASK**: Get task by display index
  - Parameters: `user_id`, `display_index`
  - Validation: Display index must exist in current mapping

## Relationships

### User-Task-Mapping Relationship
- Each user has their own display mapping context
- Mapping connects user's display_index to internal task_id
- Tasks are isolated between users
- Foreign key relationship: `user_id` → `user.id`, `task_id` → `task.id`

### Mapping Dependencies
- Display mapping depends on current task list state
- Mapping is invalidated when task list changes
- Sequential numbering depends on task order
- State changes trigger mapping updates

## Constraints and Rules

### Data Integrity
- Display indices must remain sequential and start from 1
- Each display_index must map to exactly one task_id per user
- Mapping must be refreshed when task list changes
- Invalid mappings must be handled gracefully

### Business Rules
- Users can only access their own display mappings
- Display indices are regenerated when tasks are added/removed
- Mapping state must be synchronized between UI and AI agent
- Error responses must be helpful rather than generic fallbacks