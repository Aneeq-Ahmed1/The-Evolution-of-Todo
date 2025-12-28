# Quickstart Guide: In-Memory Todo Console Application

## Prerequisites
- Python 3.13+
- uv package manager

## Setup
1. Clone the repository
2. Navigate to the project directory
3. Install dependencies: `uv sync`
4. Verify installation: `uv run python -c "import sys; print(sys.version)"`

## Usage
1. Run the application: `uv run python -m todo.main [command] [arguments]`
2. Available commands:
   - `add "Task Title" ["Description"]` - Add a new task
   - `list` - List all tasks
   - `update <id> ["New Title"] ["New Description"]` - Update task details
   - `complete <id>` - Mark task as complete
   - `uncomplete <id>` - Mark task as pending
   - `delete <id>` - Delete a task
   - `export` - Export tasks to JSON
   - `import <file>` - Import tasks from JSON file

## Example Workflow
1. Add a task: `uv run python -m todo.main add "Buy groceries" "Milk, bread, eggs"`
2. List tasks: `uv run python -m todo.main list`
3. Complete a task: `uv run python -m todo.main complete 1`
4. Update a task: `uv run python -m todo.main update 1 "Buy groceries (done)" "Milk, bread, eggs, fruits"`
5. Delete a task: `uv run python -m todo.main delete 1`

## Troubleshooting
- If you get "command not found" errors, ensure you're using the correct command format
- If you encounter import errors, run `uv sync` to ensure all dependencies are installed
- For help: `uv run python -m todo.main --help`