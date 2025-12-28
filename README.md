# In-Memory Todo Console Application

A simple command-line todo application that stores tasks in memory with automatic expiration.

## Features

- Add, view, update, complete, and delete tasks
- Task expiration after 24 hours of inactivity
- Import/export tasks in JSON format
- Command-line interface

## Requirements

- Python 3.13+
- uv package manager

## Installation

1. Install dependencies: `uv sync`
2. Run the application: `uv run python -m todo.main [command] [arguments]`

## Usage

```
todo [command] [arguments]

Available commands:
  add          Add a new task
  list         List all tasks
  update       Update a task
  complete     Mark task as complete
  uncomplete   Mark task as pending
  delete       Delete a task
  export       Export tasks to JSON
  import       Import tasks from JSON file
```

### Examples

- Add a task: `uv run python -m todo.main add "Buy groceries" "Milk, bread, eggs"`
- List tasks: `uv run python -m todo.main list`
- Complete a task: `uv run python -m todo.main complete 1`
- Update a task: `uv run python -m todo.main update 1 --title "Buy groceries (done)" --description "Milk, bread, eggs, fruits"`
- Delete a task: `uv run python -m todo.main delete 1`

## Architecture

- **CLI Layer**: Handles user input/output via command-line arguments
- **Domain Layer**: Task entity and TaskManager for business logic
- **Data Storage**: In-memory dictionary with automatic cleanup of expired tasks