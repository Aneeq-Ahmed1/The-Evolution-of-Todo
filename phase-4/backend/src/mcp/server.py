"""
MCP Server for the AI Chatbot - handles tool registration and discovery.
"""
from typing import Dict, Any, Callable
from .tools import MCPTaskTools
from sqlmodel import Session


class MCPServer:
    def __init__(self):
        self.tools: Dict[str, Callable] = {}
        self._register_tools()

    def _register_tools(self):
        """Register all available MCP tools."""
        # Note: These are placeholders that will be called with proper session
        self.tools["add_task"] = self._create_tool_handler("add_task")
        self.tools["list_tasks"] = self._create_tool_handler("list_tasks")
        self.tools["complete_task"] = self._create_tool_handler("complete_task")
        self.tools["delete_task"] = self._create_tool_handler("delete_task")
        self.tools["update_task"] = self._create_tool_handler("update_task")

    def _create_tool_handler(self, tool_name: str):
        """Create a handler that will be called with session and parameters."""
        def handler(session: Session, **kwargs):
            task_tools = MCPTaskTools(session)
            tool_method = getattr(task_tools, tool_name)
            return tool_method(**kwargs)
        return handler

    def get_tool(self, tool_name: str) -> Callable:
        """Get a registered tool by name."""
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' is not registered")
        return self.tools[tool_name]

    def list_tools(self) -> Dict[str, Any]:
        """List all available tools with their schemas."""
        schemas = {
            "add_task": {
                "name": "add_task",
                "description": "Create a new task for the specified user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The identifier of the user requesting the task creation"},
                        "title": {"type": "string", "description": "The title of the task to be created (1-255 characters)"},
                        "description": {"type": "string", "description": "An optional description for the task"}
                    },
                    "required": ["user_id", "title"]
                }
            },
            "list_tasks": {
                "name": "list_tasks",
                "description": "Retrieve a list of tasks for the specified user, with optional status filtering",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The identifier of the user whose tasks to list"},
                        "status": {"type": "string", "description": "Filter tasks by status (all, pending, completed); defaults to 'all'"}
                    },
                    "required": ["user_id"]
                }
            },
            "complete_task": {
                "name": "complete_task",
                "description": "Mark a specific task as completed for the specified user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The identifier of the user requesting the completion"},
                        "task_id": {"type": "integer", "description": "The identifier of the task to mark as completed"}
                    },
                    "required": ["user_id", "task_id"]
                }
            },
            "delete_task": {
                "name": "delete_task",
                "description": "Remove a specific task from the user's task list",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The identifier of the user requesting the deletion"},
                        "task_id": {"type": "integer", "description": "The identifier of the task to delete"}
                    },
                    "required": ["user_id", "task_id"]
                }
            },
            "update_task": {
                "name": "update_task",
                "description": "Modify the title and/or description of a specific task for the specified user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The identifier of the user requesting the update"},
                        "task_id": {"type": "integer", "description": "The identifier of the task to update"},
                        "title": {"type": "string", "description": "New title for the task (if provided)"},
                        "description": {"type": "string", "description": "New description for the task (if provided)"}
                    },
                    "required": ["user_id", "task_id"]
                }
            }
        }
        return schemas


# Global MCP server instance
mcp_server = MCPServer()