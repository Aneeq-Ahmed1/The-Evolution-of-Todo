# CLI Contract: In-Memory Todo Console Application

## Command Structure
```
todo [command] [arguments]
```

## Commands

### `add`
**Description**: Add a new task
**Usage**: `todo add "Task Title" ["Description"]`
**Arguments**:
- title (required): Task title (max 200 chars)
- description (optional): Task description (max 1000 chars)
**Return**: Task ID of created task
**Errors**: Returns error if title is empty or exceeds length limits

### `list`
**Description**: List all tasks
**Usage**: `todo list`
**Arguments**: None
**Return**: List of tasks with ID, title, and status
**Errors**: None

### `update`
**Description**: Update task details
**Usage**: `todo update <id> ["New Title"] ["New Description"]`
**Arguments**:
- id (required): Task ID
- title (optional): New task title
- description (optional): New task description
**Return**: Confirmation of update
**Errors**: Returns error if task ID doesn't exist

### `complete`
**Description**: Mark task as complete
**Usage**: `todo complete <id>`
**Arguments**:
- id (required): Task ID
**Return**: Confirmation of completion
**Errors**: Returns error if task ID doesn't exist

### `uncomplete`
**Description**: Mark task as pending
**Usage**: `todo uncomplete <id>`
**Arguments**:
- id (required): Task ID
**Return**: Confirmation of status change
**Errors**: Returns error if task ID doesn't exist

### `delete`
**Description**: Delete a task
**Usage**: `todo delete <id>`
**Arguments**:
- id (required): Task ID
**Return**: Confirmation of deletion
**Errors**: Returns error if task ID doesn't exist

### `export`
**Description**: Export tasks to JSON
**Usage**: `todo export`
**Arguments**: None
**Return**: JSON string of all tasks
**Errors**: None

### `import`
**Description**: Import tasks from JSON file
**Usage**: `todo import <file>`
**Arguments**:
- file (required): Path to JSON file
**Return**: Confirmation of import
**Errors**: Returns error if file is invalid or doesn't exist