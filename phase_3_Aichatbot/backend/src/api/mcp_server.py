"""
Model Context Protocol (MCP) Server for the AI Agent Platform
Implements MCP tools for task management and other capabilities
"""
import asyncio
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import uuid
from sqlmodel import Session
from uuid import UUID

from ..models.conversation import Conversation
from ..models.message import Message
from ..services.conversation_service import ConversationService
from ..db.database import get_session
from ..utils.logging import Logger
from ..auth.auth_handler import get_current_user, TokenData


router = APIRouter(prefix="/api/mcp", tags=["mcp"])


class MCPCallRequest(BaseModel):
    """Request model for MCP tool calls"""
    tool_name: str
    parameters: Dict[str, Any]


class MCPCallResponse(BaseModel):
    """Response model for MCP tool calls"""
    success: bool
    result: Optional[Any] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = {}


class TaskCreateRequest(BaseModel):
    """Request model for creating a task"""
    title: str
    description: Optional[str] = None
    status: str = "pending"
    user_id: str


class TaskUpdateRequest(BaseModel):
    """Request model for updating a task"""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


@router.post("/tools/call", response_model=MCPCallResponse)
async def call_mcp_tool(
    request: MCPCallRequest,
    current_user: TokenData = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> MCPCallResponse:
    """
    MCP tool endpoint that allows the AI agent to call various tools
    Implements task management and other MCP-compatible tools
    Implements FR-013: System MUST implement user authentication with session management for multi-user support and conversation privacy
    """
    try:
        Logger.info(f"MCP tool called: {request.tool_name} with params: {request.parameters} by user: {current_user.user_id}")

        # Use the authenticated user's ID and the provided session
        user_id = current_user.user_id
        conversation_service = ConversationService(session)

        # Route to appropriate tool based on tool_name
        if request.tool_name == "create_task":
            return await _handle_create_task(request.parameters, user_id, session)
        elif request.tool_name == "list_tasks":
            return await _handle_list_tasks(request.parameters, user_id, session)
        elif request.tool_name == "update_task":
            return await _handle_update_task(request.parameters, user_id, session)
        elif request.tool_name == "delete_task":
            return await _handle_delete_task(request.parameters, user_id, session)
        elif request.tool_name == "get_conversation_history":
            return await _handle_get_conversation_history(request.parameters, conversation_service)
        else:
            return MCPCallResponse(
                success=False,
                error=f"Unknown tool: {request.tool_name}",
                metadata={"available_tools": [
                    "create_task", "list_tasks", "update_task", "delete_task", "get_conversation_history"
                ]}
            )

    except Exception as e:
        Logger.error(f"Error in MCP tool call: {str(e)}")
        return MCPCallResponse(
            success=False,
            error=str(e),
            metadata={}
        )


async def _handle_create_task(params: Dict[str, Any], user_id: str, session: Session) -> MCPCallResponse:
    """Handle create_task MCP tool call"""
    try:
        # Import the Task model and TaskService
        from ...models import Task
        from ...services.task_service import TaskService
        from ...schemas import TaskCreateRequest as SchemaTaskCreateRequest
        
        # Prepare task creation data
        task_create_request = SchemaTaskCreateRequest(
            title=params.get("title", ""),
            description=params.get("description", "")
        )
        
        # Use the TaskService to create the task in the database
        created_task = TaskService.create_task(session, user_id, task_create_request)
        
        # Convert to the expected response format
        task_result = {
            "id": created_task.id,
            "title": created_task.title,
            "description": created_task.description,
            "completed": created_task.completed,
            "user_id": created_task.user_id,
            "created_at": created_task.created_at.isoformat() if hasattr(created_task, 'created_at') else None,
            "updated_at": created_task.updated_at.isoformat() if hasattr(created_task, 'updated_at') else None
        }

        return MCPCallResponse(
            success=True,
            result=task_result,
            metadata={"action": "create_task", "task_id": created_task.id}
        )
    except Exception as e:
        Logger.error(f"Error in _handle_create_task: {str(e)}")
        return MCPCallResponse(
            success=False,
            error=f"Failed to create task: {str(e)}",
            metadata={"action": "create_task"}
        )


async def _handle_list_tasks(params: Dict[str, Any], user_id: str, session: Session) -> MCPCallResponse:
    """Handle list_tasks MCP tool call"""
    try:
        # Import the TaskService
        from ...services.task_service import TaskService
        
        # Get status filter from params, default to "all"
        status_filter = params.get("status", "all")
        
        # Use the TaskService to get tasks from the database
        tasks = TaskService.get_tasks_by_user(session, user_id, status_filter)
        
        # Convert to the expected response format
        tasks_result = []
        for task in tasks:
            task_dict = {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "user_id": task.user_id,
                "created_at": task.created_at.isoformat() if hasattr(task, 'created_at') else None,
                "updated_at": task.updated_at.isoformat() if hasattr(task, 'updated_at') else None
            }
            tasks_result.append(task_dict)

        return MCPCallResponse(
            success=True,
            result=tasks_result,
            metadata={"action": "list_tasks", "count": len(tasks_result)}
        )
    except Exception as e:
        Logger.error(f"Error in _handle_list_tasks: {str(e)}")
        return MCPCallResponse(
            success=False,
            error=f"Failed to list tasks: {str(e)}",
            metadata={"action": "list_tasks"}
        )


async def _handle_update_task(params: Dict[str, Any], user_id: str, session: Session) -> MCPCallResponse:
    """Handle update_task MCP tool call"""
    try:
        if "task_id" not in params:
            return MCPCallResponse(
                success=False,
                error="task_id is required for update_task",
                metadata={"action": "update_task"}
            )

        task_id = int(params["task_id"])  # Convert to int since the DB uses integer IDs
        
        # Import the TaskService and models
        from ...services.task_service import TaskService
        from ...models import TaskUpdate
        
        # Prepare update data - only include fields that are provided
        update_data = {}
        if "title" in params and params["title"] is not None:
            update_data["title"] = params["title"]
        if "description" in params and params["description"] is not None:
            update_data["description"] = params["description"]
        if "completed" in params and params["completed"] is not None:
            update_data["completed"] = params["completed"]
        elif "status" in params and params["status"] is not None:
            # Map status to completed boolean
            update_data["completed"] = params["status"] == "completed"
        
        # Create TaskUpdate object with only the fields to update
        task_update = TaskUpdate(**{k: v for k, v in update_data.items()})
        
        # Use the TaskService to update the task in the database
        updated_task = TaskService.update_task(session, task_id, user_id, task_update)
        
        if not updated_task:
            return MCPCallResponse(
                success=False,
                error=f"Task with id {task_id} not found or you don't have permission to update it",
                metadata={"action": "update_task", "task_id": task_id}
            )
        
        # Convert to the expected response format
        task_result = {
            "id": updated_task.id,
            "title": updated_task.title,
            "description": updated_task.description,
            "completed": updated_task.completed,
            "user_id": updated_task.user_id,
            "created_at": updated_task.created_at.isoformat() if hasattr(updated_task, 'created_at') else None,
            "updated_at": updated_task.updated_at.isoformat() if hasattr(updated_task, 'updated_at') else None
        }

        return MCPCallResponse(
            success=True,
            result=task_result,
            metadata={"action": "update_task", "task_id": task_id}
        )
    except ValueError:
        return MCPCallResponse(
            success=False,
            error="task_id must be a valid integer",
            metadata={"action": "update_task"}
        )
    except Exception as e:
        Logger.error(f"Error in _handle_update_task: {str(e)}")
        return MCPCallResponse(
            success=False,
            error=f"Failed to update task: {str(e)}",
            metadata={"action": "update_task"}
        )


async def _handle_delete_task(params: Dict[str, Any], user_id: str, session: Session) -> MCPCallResponse:
    """Handle delete_task MCP tool call"""
    try:
        if "task_id" not in params:
            return MCPCallResponse(
                success=False,
                error="task_id is required for delete_task",
                metadata={"action": "delete_task"}
            )

        task_id = int(params["task_id"])  # Convert to int since the DB uses integer IDs
        
        # Import the TaskService
        from ...services.task_service import TaskService
        
        # Use the TaskService to delete the task from the database
        success = TaskService.delete_task(session, task_id, user_id)
        
        if not success:
            return MCPCallResponse(
                success=False,
                error=f"Task with id {task_id} not found or you don't have permission to delete it",
                metadata={"action": "delete_task", "task_id": task_id}
            )

        return MCPCallResponse(
            success=True,
            result={"message": f"Task {task_id} deleted successfully"},
            metadata={"action": "delete_task", "task_id": task_id}
        )
    except ValueError:
        return MCPCallResponse(
            success=False,
            error="task_id must be a valid integer",
            metadata={"action": "delete_task"}
        )
    except Exception as e:
        Logger.error(f"Error in _handle_delete_task: {str(e)}")
        return MCPCallResponse(
            success=False,
            error=f"Failed to delete task: {str(e)}",
            metadata={"action": "delete_task"}
        )


async def _handle_get_conversation_history(params: Dict[str, Any], conversation_service: ConversationService) -> MCPCallResponse:
    """Handle get_conversation_history MCP tool call"""
    try:
        if "conversation_id" not in params:
            return MCPCallResponse(
                success=False,
                error="conversation_id is required for get_conversation_history",
                metadata={"action": "get_conversation_history"}
            )

        conversation_id = UUID(params["conversation_id"])

        # Get the conversation and its messages
        conversation = await conversation_service.get_conversation(conversation_id)
        if not conversation:
            return MCPCallResponse(
                success=False,
                error=f"Conversation with id {params['conversation_id']} not found",
                metadata={"action": "get_conversation_history", "conversation_id": params["conversation_id"]}
            )

        messages = await conversation_service.get_messages_for_conversation(conversation_id)

        history = []
        for msg in messages:
            history.append({
                "id": str(msg.id),
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat() if msg.timestamp else None
            })

        return MCPCallResponse(
            success=True,
            result={
                "conversation": {
                    "id": str(conversation.id),
                    "title": conversation.title,
                    "created_at": conversation.created_at.isoformat() if conversation.created_at else None,
                    "updated_at": conversation.updated_at.isoformat() if conversation.updated_at else None
                },
                "messages": history,
                "message_count": len(history)
            },
            metadata={"action": "get_conversation_history", "conversation_id": params["conversation_id"]}
        )
    except Exception as e:
        return MCPCallResponse(
            success=False,
            error=f"Failed to get conversation history: {str(e)}",
            metadata={"action": "get_conversation_history"}
        )


# Health check for MCP server
@router.get("/health")
async def mcp_health_check() -> Dict[str, str]:
    """
    Health check endpoint for MCP server
    """
    return {"status": "healthy", "service": "mcp-server", "tools_available": len([
        "create_task", "list_tasks", "update_task", "delete_task", "get_conversation_history"
    ])}