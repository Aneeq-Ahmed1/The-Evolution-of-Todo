# Todo Evolution - Phase I Usage Guide

## Overview
Todo Evolution - Phase I is a simple, in-memory console-based todo application that allows users to manage their tasks through a command-line interface. All data is stored in memory and will be lost when the application closes.

## Getting Started

### Running the Application
To run the application, execute:

```bash
python -m src.todo_app
```

Or if you have it installed as a package:
```bash
todo-app
```

## Features

### 1. Add Task
- Select option 1 from the main menu
- Enter a title and description for your task
- The system will assign a unique ID to your task
- You'll receive confirmation once the task is added

### 2. View All Tasks
- Select option 2 from the main menu
- All tasks will be displayed with their ID, title, description, and status
- Status indicators:
  - [○] - Pending/Incomplete
  - [✓] - Complete

### 3. Update Task
- Select option 3 from the main menu
- Enter the ID of the task you want to update
- You'll see the current details and can provide new values
- Leave fields blank to keep current values

### 4. Delete Task
- Select option 4 from the main menu
- Enter the ID of the task you want to delete
- You'll be asked to confirm the deletion
- The task will be permanently removed

### 5. Mark Task Complete/Incomplete
- Select option 5 to mark a task as complete
- Select option 6 to mark a task as incomplete
- Enter the ID of the task you want to update
- The status will be changed and confirmed

## Best Practices

### Task Management
- Use descriptive titles for easy identification
- Include detailed descriptions for complex tasks
- Regularly review and update task statuses
- Remove completed tasks to keep the list manageable

### Performance
- The application is optimized for a moderate number of tasks
- For large numbers of tasks, consider breaking them into smaller groups
- Remember that all data is temporary and will be lost on exit

## Limitations

### In-Memory Storage
- All tasks are stored only in memory
- Data is lost when the application closes
- No persistent storage is implemented in Phase I

### Single Session
- The application supports only one user session at a time
- No multi-user functionality is available in Phase I