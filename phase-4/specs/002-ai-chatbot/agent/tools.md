# MCP Tools Specification: Todo AI Chatbot

## Overview
This document specifies the Model Context Protocol (MCP) tools available to the AI agent for todo management operations. Each tool follows a stateless design pattern and interacts with the PostgreSQL database for data persistence.

## Tool: add_task

### Purpose
Create a new task for the specified user.

### Parameters
- `user_id` (string, required): The identifier of the user requesting the task creation
- `title` (string, required): The title of the task to be created (1-255 characters)
- `description` (string, optional): An optional description for the task

### Response
- `task_id` (integer): The unique identifier of the created task
- `status` (string): The status of the created task ("pending")
- `title` (string): The title of the created task

### Validation
- `user_id` must match the authenticated user
- `title` must be provided and 1-255 characters
- Task is created with `completed` set to `false` by default

### Error Handling
- Returns error if `title` is missing or invalid
- Returns error if database operation fails
- Returns error if user authentication is invalid

## Tool: list_tasks

### Purpose
Retrieve a list of tasks for the specified user, with optional status filtering.

### Parameters
- `user_id` (string, required): The identifier of the user whose tasks to list
- `status` (string, optional): Filter tasks by status ("all", "pending", "completed"; defaults to "all")

### Response
- `tasks` (array): List of task objects with the following properties:
  - `id` (integer): Unique identifier of the task
  - `title` (string): Title of the task
  - `description` (string): Description of the task (may be null)
  - `completed` (boolean): Whether the task is completed
  - `created_at` (string): Timestamp when the task was created

### Validation
- `user_id` must match the authenticated user
- `status` must be one of the allowed values if provided

### Error Handling
- Returns error if `user_id` is invalid
- Returns empty array if no tasks found
- Returns error if database operation fails

## Tool: complete_task

### Purpose
Mark a specific task as completed for the specified user.

### Parameters
- `user_id` (string, required): The identifier of the user requesting the completion
- `task_id` (integer, required): The identifier of the task to mark as completed

### Response
- `task_id` (integer): The identifier of the completed task
- `status` (string): The status of the task ("completed")
- `title` (string): The title of the completed task

### Validation
- `user_id` must match the authenticated user
- `task_id` must exist and belong to the user
- Task must not already be completed

### Error Handling
- Returns error if `task_id` does not exist
- Returns error if task does not belong to the user
- Returns error if database operation fails

## Tool: delete_task

### Purpose
Remove a specific task from the user's task list.

### Parameters
- `user_id` (string, required): The identifier of the user requesting the deletion
- `task_id` (integer, required): The identifier of the task to delete

### Response
- `task_id` (integer): The identifier of the deleted task
- `status` (string): Confirmation of deletion ("deleted")
- `title` (string): The title of the deleted task

### Validation
- `user_id` must match the authenticated user
- `task_id` must exist and belong to the user

### Error Handling
- Returns error if `task_id` does not exist
- Returns error if task does not belong to the user
- Returns error if database operation fails

## Tool: update_task

### Purpose
Modify the title and/or description of a specific task for the specified user.

### Parameters
- `user_id` (string, required): The identifier of the user requesting the update
- `task_id` (integer, required): The identifier of the task to update
- `title` (string, optional): New title for the task (if provided)
- `description` (string, optional): New description for the task (if provided)

### Response
- `task_id` (integer): The identifier of the updated task
- `status` (string): The status of the updated task ("pending" or "completed")
- `title` (string): The updated title of the task

### Validation
- `user_id` must match the authenticated user
- `task_id` must exist and belong to the user
- If `title` is provided, it must be 1-255 characters

### Error Handling
- Returns error if `task_id` does not exist
- Returns error if task does not belong to the user
- Returns error if `title` is invalid (if provided)
- Returns error if database operation fails

## MCP Server Configuration

### Protocol Compliance
- Implements MCP specification for tool discovery
- Provides proper tool schemas as defined above
- Handles tool execution requests from the AI agent
- Returns properly formatted responses

### Security
- Validates user authentication for each tool call
- Ensures data isolation between users
- Implements proper input validation
- Logs tool usage for monitoring

### Error Reporting
- Provides clear error messages to the AI agent
- Maintains proper HTTP status codes
- Includes error context for debugging
- Prevents exposure of internal system details