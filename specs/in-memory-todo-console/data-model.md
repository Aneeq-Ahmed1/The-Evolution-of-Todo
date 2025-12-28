# Data Model: In-Memory Todo Console Application

## Task Entity

### Attributes
- **id**: integer (auto-increment starting from 1)
- **title**: string (required, max 200 characters)
- **description**: string | null (optional, max 1000 characters)
- **completed**: boolean (default: false)
- **created_at**: datetime (for expiration tracking)
- **last_accessed**: datetime (for expiration tracking)

### Validation Rules
- title: Required, non-empty, maximum 200 characters
- description: Optional, maximum 1000 characters
- completed: Boolean value, defaults to false

## TaskList Entity

### Attributes
- **tasks**: dict (key: task_id, value: Task object)
- **next_id**: integer (next auto-increment ID)
- **expiration_hours**: integer (default: 24)

### State Transitions
- Task status can transition between 'pending' and 'completed'
- Task can be created (pending), updated, completed, uncompleted, or deleted
- Task expires after 24 hours of inactivity

## Relationships
- TaskList contains multiple Task entities
- Each Task has a unique ID within the TaskList