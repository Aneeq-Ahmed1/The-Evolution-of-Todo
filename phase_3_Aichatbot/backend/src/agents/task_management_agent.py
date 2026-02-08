"""
Task Management Agent for the AI Agent Platform
Handles task management operations using MCP tools
"""
from typing import Dict, Any, Optional
from ..models.message import MessageCreate
from ..services.conversation_service import ConversationService
from .base_agent import BaseAgent, AgentResponse
from ..providers.base_provider import BaseProvider, Message as ProviderMessage
from ..utils.logging import log_provider_call, Logger
from ..db.settings import settings
import asyncio
import httpx
import json


class TaskManagementAgent(BaseAgent):
    """
    The task management agent is responsible for:
    1. Handling task-related user requests
    2. Converting natural language to MCP tool calls
    3. Managing task CRUD operations
    4. Providing natural language responses
    """

    def __init__(self, conversation_service: ConversationService, provider: BaseProvider):
        super().__init__(conversation_service)

        # Provider for LLM interactions
        self.provider = provider

        # Validate provider configuration
        if not self.provider.validate_config():
            raise ValueError("Invalid provider configuration")

        # Define task-related intents
        self.task_intents = {
            "create_task": [
                r"\b(add|create|make|new|build)\s+(a\s+)?(task|todo|item|thing|note)\b",
                r"\b(need to|want to|should|must)\s+(add|create|make|build)\s+(a\s+)?(task|todo|item|thing|note)\b",
                r"\b(remind me to|remember to)\b"
            ],
            "list_tasks": [
                r"\b(list|show|display|view|see|get)\s+(my\s+)?(tasks|todos|items|things|notes)\b",
                r"\b(what['’]?\s*(are|is)\s*(my\s+)?(tasks|todos|items|things|notes))\b",
                r"\b(did i|have i)\s+(any\s+)?(tasks|todos|items|things|notes)\b"
            ],
            "complete_task": [
                r"\b(complete|finish|done|accomplish|achieve)\s+(a\s+)?(task|todo|item|thing|note)\b",
                r"\b(mark|set)\s+(as\s+)?(complete|done|finished)\b",
                r"\b(done with|finished with)\s+(a\s+)?(task|todo|item|thing|note)\b"
            ],
            "delete_task": [
                r"\b(delete|remove|erase|eliminate|cancel)\s+(a\s+)?(task|todo|item|thing|note)\b",
                r"\b(get rid of|throw away|dispose of)\s+(a\s+)?(task|todo|item|thing|note)\b"
            ],
            "update_task": [
                r"\b(update|change|modify|edit|adjust)\s+(a\s+)?(task|todo|item|thing|note)\b",
                r"\b(change|update|modify|edit|adjust)\s+(the\s+)?(title|description|details)\b"
            ]
        }

    def get_agent_type(self) -> str:
        """Return the type of agent"""
        return "task_management"

    async def process(self, message: str, conversation_id: str, user_id: str) -> AgentResponse:
        """
        Process a user message and generate a task management response

        Args:
            message: The user's input message
            conversation_id: ID of the conversation
            user_id: ID of the user

        Returns:
            AgentResponse: The agent's response with metadata
        """
        try:
            # Log the incoming request
            Logger.info(f"Task management agent processing message: {message[:50]}...",
                       extra={"conversation_id": conversation_id, "user_id": user_id})

            # Add the user's message to the conversation
            user_message = MessageCreate(role="user", content=message)
            await self.conversation_service.add_message_to_conversation(conversation_id, user_message)

            # Determine if this is a task-related request
            intent = self._detect_task_intent(message)
            
            if intent:
                # Process as a task management request
                response = await self._handle_task_request(intent, message, user_id)
                
                # Add the assistant's response to the conversation
                assistant_message = MessageCreate(
                    role="assistant",
                    content=response
                )
                await self.conversation_service.add_message_to_conversation(conversation_id, assistant_message)

                return AgentResponse(
                    content=response,
                    metadata={
                        "agent_type": self.get_agent_type(),
                        "intent": intent,
                        "handled_by_task_agent": True
                    }
                )
            else:
                # Not a task-related request, defer to general conversation
                return await self._handle_general_conversation(message, conversation_id, user_id)

        except Exception as e:
            Logger.error(f"Error in task management agent: {str(e)}", 
                         extra={"user_id": user_id, "conversation_id": conversation_id})

            return AgentResponse(
                content="I'm sorry, I encountered an error while processing your request. Please try again.",
                error=str(e),
                metadata={"error_occurred": True}
            )

    def _detect_task_intent(self, message: str) -> Optional[str]:
        """
        Detect if the message is related to task management

        Args:
            message: The user's message

        Returns:
            str or None: The detected intent or None if not a task-related message
        """
        import re
        
        message_lower = message.lower()
        
        for intent, patterns in self.task_intents.items():
            for pattern in patterns:
                if re.search(pattern, message_lower):
                    return intent
        
        return None

    async def _handle_task_request(self, intent: str, message: str, user_id: str) -> str:
        """
        Handle a task management request by calling the appropriate MCP tool

        Args:
            intent: The detected intent
            message: The original user message
            user_id: The user ID

        Returns:
            str: The response to the user
        """
        try:
            # Prepare parameters for the MCP tool call
            params = await self._extract_task_params(intent, message)
            params["user_id"] = user_id  # Ensure we use the authenticated user's ID

            # Call the appropriate MCP tool
            if intent == "create_task":
                return await self._call_create_task(params)
            elif intent == "list_tasks":
                return await self._call_list_tasks(params)
            elif intent == "complete_task":
                return await self._call_complete_task(params)
            elif intent == "delete_task":
                return await self._call_delete_task(params)
            elif intent == "update_task":
                return await self._call_update_task(params)
            else:
                return f"I understand you want to {intent.replace('_', ' ')}, but I'm not sure how to help with that."

        except Exception as e:
            Logger.error(f"Error handling task request: {str(e)}")
            return f"I'm sorry, I encountered an error while processing your request: {str(e)}"

    async def _extract_task_params(self, intent: str, message: str) -> Dict[str, Any]:
        """
        Extract parameters from the user message based on the intent

        Args:
            intent: The detected intent
            message: The user's message

        Returns:
            Dict[str, Any]: Extracted parameters
        """
        import re
        
        params = {}
        
        if intent == "create_task":
            # Extract task title from message
            # Look for text after common task creation phrases
            patterns = [
                r"(?:add|create|make|new|build)\s+(?:a\s+)?(?:task|todo|item|thing|note)\s+(.+?)(?:\.|$)",
                r"(?:need to|want to|should|must)\s+(?:add|create|make|build)\s+(?:a\s+)?(?:task|todo|item|thing|note)\s+(.+?)(?:\.|$)",
                r"(?:remind me to|remember to)\s+(.+?)(?:\.|$)"
            ]
            
            for pattern in patterns:
                match = re.search(pattern, message.lower())
                if match:
                    title = match.group(1).strip()
                    if title:
                        params["title"] = title
                        break
            
            # If no title was extracted, use the whole message as title
            if not params.get("title"):
                # Clean up the message to extract a meaningful title
                clean_msg = re.sub(r'(add|create|make|new|build|task|todo|item|thing|note)', '', message, flags=re.IGNORECASE)
                clean_msg = clean_msg.strip()
                if clean_msg:
                    params["title"] = clean_msg[:100]  # Limit title length
                else:
                    params["title"] = "Untitled task"
        
        elif intent == "complete_task":
            # Extract task ID or title to identify which task to complete
            # This is more complex and would require looking up tasks by title or having the user specify an ID
            # For now, we'll just note that the user wants to complete a task
            pass
        
        elif intent == "delete_task":
            # Similar to complete_task, extract which task to delete
            pass
        
        elif intent == "update_task":
            # Extract which task to update and what to update
            pass
        
        elif intent == "list_tasks":
            # Check if user wants specific status
            if "completed" in message.lower():
                params["status"] = "completed"
            elif "pending" in message.lower() or "incomplete" in message.lower():
                params["status"] = "pending"
        
        return params

    async def _call_create_task(self, params: Dict[str, Any]) -> str:
        """
        Call the create_task MCP tool

        Args:
            params: Parameters for the tool call

        Returns:
            str: Response from the tool
        """
        try:
            # Use the session from the conversation service
            from ..api.mcp_server import _handle_create_task
            
            # Call the handler directly with the session from conversation service
            result = await _handle_create_task(params, params["user_id"], self.conversation_service.session)
            
            if result.success:
                task = result.result
                return f"I've created the task '{task['title']}' for you."
            else:
                error = result.error or "Unknown error"
                return f"Sorry, I couldn't create the task: {error}"
                
        except Exception as e:
            Logger.error(f"Error calling create_task MCP tool: {str(e)}")
            return f"Sorry, I encountered an error while creating the task: {str(e)}"

    async def _call_list_tasks(self, params: Dict[str, Any]) -> str:
        """
        Call the list_tasks MCP tool

        Args:
            params: Parameters for the tool call

        Returns:
            str: Response from the tool
        """
        try:
            # Use the session from the conversation service
            from ..api.mcp_server import _handle_list_tasks
            
            # Call the handler directly with the session from conversation service
            result = await _handle_list_tasks(params, params["user_id"], self.conversation_service.session)
            
            if result.success:
                tasks = result.result
                if tasks:
                    task_list = "\n".join([f"- {task['title']}" for task in tasks])
                    status = params.get("status", "all")
                    return f"Here are your {status} tasks:\n{task_list}"
                else:
                    status = params.get("status", "all")
                    return f"You don't have any {status} tasks right now."
            else:
                error = result.error or "Unknown error"
                return f"Sorry, I couldn't list your tasks: {error}"
                
        except Exception as e:
            Logger.error(f"Error calling list_tasks MCP tool: {str(e)}")
            return f"Sorry, I encountered an error while listing your tasks: {str(e)}"

    async def _call_complete_task(self, params: Dict[str, Any]) -> str:
        """
        Call the update_task MCP tool to mark a task as complete

        Args:
            params: Parameters for the tool call

        Returns:
            str: Response from the tool
        """
        try:
            # Use the session from the conversation service
            from ..api.mcp_server import _handle_update_task
            
            # Add completed status to params
            params["completed"] = True
            
            # Call the handler directly with the session from conversation service
            result = await _handle_update_task(params, params["user_id"], self.conversation_service.session)
            
            if result.success:
                task = result.result
                return f"I've marked the task '{task['title']}' as complete."
            else:
                error = result.error or "Unknown error"
                return f"Sorry, I couldn't complete the task: {error}"
                
        except Exception as e:
            Logger.error(f"Error calling complete_task MCP tool: {str(e)}")
            return f"Sorry, I encountered an error while completing the task: {str(e)}"

    async def _call_delete_task(self, params: Dict[str, Any]) -> str:
        """
        Call the delete_task MCP tool

        Args:
            params: Parameters for the tool call

        Returns:
            str: Response from the tool
        """
        try:
            # Use the session from the conversation service
            from ..api.mcp_server import _handle_delete_task
            
            # Call the handler directly with the session from conversation service
            result = await _handle_delete_task(params, params["user_id"], self.conversation_service.session)
            
            if result.success:
                return f"I've deleted the task successfully."
            else:
                error = result.error or "Unknown error"
                return f"Sorry, I couldn't delete the task: {error}"
                
        except Exception as e:
            Logger.error(f"Error calling delete_task MCP tool: {str(e)}")
            return f"Sorry, I encountered an error while deleting the task: {str(e)}"

    async def _call_update_task(self, params: Dict[str, Any]) -> str:
        """
        Call the update_task MCP tool

        Args:
            params: Parameters for the tool call

        Returns:
            str: Response from the tool
        """
        try:
            # Use the session from the conversation service
            from ..api.mcp_server import _handle_update_task
            
            # Call the handler directly with the session from conversation service
            result = await _handle_update_task(params, params["user_id"], self.conversation_service.session)
            
            if result.success:
                task = result.result
                return f"I've updated the task '{task['title']}' for you."
            else:
                error = result.error or "Unknown error"
                return f"Sorry, I couldn't update the task: {error}"
                
        except Exception as e:
            Logger.error(f"Error calling update_task MCP tool: {str(e)}")
            return f"Sorry, I encountered an error while updating the task: {str(e)}"

    async def _handle_general_conversation(self, message: str, conversation_id: str, user_id: str) -> AgentResponse:
        """
        Handle a general conversation request using the LLM provider

        Args:
            message: The user's input message
            conversation_id: ID of the conversation
            user_id: ID of the user

        Returns:
            AgentResponse: The agent's response with metadata
        """
        try:
            # Retrieve conversation history to maintain context
            conversation_history = await self.conversation_service.get_conversation_history(conversation_id)

            # Convert conversation history to provider messages
            provider_messages = []
            for msg in conversation_history:
                provider_messages.append(ProviderMessage(
                    role=msg.role,
                    content=msg.content
                ))

            # Add the current message if not already in history
            if not any(m.content == message for m in provider_messages):
                provider_messages.append(ProviderMessage(
                    role="user",
                    content=message
                ))

            # Generate response from the provider
            provider_response = await self.provider.generate_response(
                messages=provider_messages,
                max_tokens=settings.MAX_TOKENS,
                temperature=settings.TEMPERATURE
            )

            if provider_response.error:
                Logger.error(f"Provider error: {provider_response.error}")
                return AgentResponse(
                    content=f"I'm experiencing difficulties connecting to the AI service. Error: {provider_response.error}",
                    error=provider_response.error,
                    metadata={"provider_error": True}
                )

            # Log the provider call
            log_provider_call(
                provider=settings.LLM_PROVIDER,
                model=self.provider.model_name or "default",
                tokens_used=len(provider_response.content.split())  # Rough token estimation
            )

            # Return the response
            return AgentResponse(
                content=provider_response.content,
                metadata={
                    "agent_type": self.get_agent_type(),
                    "provider_used": settings.LLM_PROVIDER,
                    "model_used": self.provider.model_name or "default",
                    "handled_by_task_agent": False
                }
            )

        except Exception as e:
            Logger.error(f"Error in general conversation handling: {str(e)}", 
                         extra={"user_id": user_id, "conversation_id": conversation_id})

            return AgentResponse(
                content="I'm sorry, I encountered an error while processing your request. Please try again.",
                error=str(e),
                metadata={"error_occurred": True}
            )