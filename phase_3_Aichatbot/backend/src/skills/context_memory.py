"""
Context memory skill for the AI Agent Platform
Manages conversation context and state for continuity
"""
from typing import Dict, Any, List, Optional
from .base_skill import BaseSkill, SkillResult
from ..utils.logging import Logger
from ..services.conversation_service import ConversationService
from ..models.message import MessageRead
import json
import hashlib


class ContextMemorySkill(BaseSkill):
    """
    The context memory skill is responsible for:
    1. Retrieving and managing conversation context
    2. Maintaining state across conversation turns
    3. Providing historical context to agents
    4. Managing context window for token efficiency
    """

    def __init__(self, conversation_service: ConversationService):
        """
        Initialize the context memory skill

        Args:
            conversation_service: Service to handle conversation persistence
        """
        self.conversation_service = conversation_service

        # Default context window settings
        self.default_context_window = 10  # Number of messages to retrieve
        self.max_context_tokens = 2048   # Maximum tokens for context window

    def get_skill_name(self) -> str:
        """Return the name of the skill"""
        return "context_memory"

    def get_required_params(self) -> list:
        """Get the list of required parameters for this skill"""
        return ["conversation_id"]

    def get_optional_params(self) -> list:
        """Get the list of optional parameters for this skill"""
        return ["context_window", "include_summary", "filter_roles"]

    async def execute(self, params: Dict[str, Any]) -> SkillResult:
        """
        Execute the context memory retrieval

        Args:
            params: Parameters for the skill execution, must include 'conversation_id',
                   optionally 'context_window', 'include_summary', 'filter_roles'

        Returns:
            SkillResult: Result of the context memory operation
        """
        try:
            # Validate parameters
            if "conversation_id" not in params:
                return SkillResult(
                    success=False,
                    error="Missing 'conversation_id' parameter"
                )

            conversation_id = params["conversation_id"]
            context_window = params.get("context_window", self.default_context_window)
            include_summary = params.get("include_summary", False)
            filter_roles = params.get("filter_roles", [])  # e.g., ["user", "assistant"]

            # Retrieve conversation history
            messages = await self.conversation_service.get_conversation_history(
                conversation_id, limit=context_window
            )

            if not messages:
                return SkillResult(
                    success=True,
                    data={
                        "context_messages": [],
                        "summary": "",
                        "has_context": False,
                        "conversation_id": conversation_id
                    }
                )

            # Filter messages by role if specified
            if filter_roles:
                filtered_messages = [msg for msg in messages if msg.role in filter_roles]
            else:
                filtered_messages = messages

            # Prepare context data
            context_data = {
                "context_messages": [
                    {
                        "role": msg.role,
                        "content": msg.content,
                        "timestamp": msg.timestamp.isoformat() if msg.timestamp else None
                    } for msg in filtered_messages
                ],
                "has_context": len(filtered_messages) > 0,
                "conversation_id": conversation_id,
                "message_count": len(filtered_messages)
            }

            # Generate summary if requested
            if include_summary:
                context_data["summary"] = await self._generate_summary(filtered_messages)
            else:
                context_data["summary"] = ""

            Logger.info(f"Context retrieved for conversation {conversation_id}", extra={
                "message_count": len(filtered_messages),
                "context_window": context_window
            })

            return SkillResult(
                success=True,
                data=context_data
            )

        except Exception as e:
            Logger.error(f"Error in context memory skill: {str(e)}")
            return SkillResult(
                success=False,
                error=f"Failed to retrieve context: {str(e)}"
            )

    async def _generate_summary(self, messages: List[MessageRead]) -> str:
        """
        Generate a summary of the conversation context

        Args:
            messages: List of messages to summarize

        Returns:
            str: Summary of the conversation
        """
        if not messages:
            return ""

        try:
            # Create a simple summary by concatenating key messages
            # In a more advanced implementation, this could use an LLM to generate summaries
            user_messages = [msg.content for msg in messages if msg.role == "user"]
            assistant_messages = [msg.content for msg in messages if msg.role == "assistant"]

            summary_parts = []

            if user_messages:
                # Add first and last user messages
                if len(user_messages) == 1:
                    summary_parts.append(f"User said: {user_messages[0][:100]}...")
                else:
                    summary_parts.append(f"User started with: {user_messages[0][:50]}...")
                    if len(user_messages) > 1:
                        summary_parts.append(f"Latest user input: {user_messages[-1][:50]}...")

            if assistant_messages:
                # Add last assistant response
                summary_parts.append(f"Assistant replied: {assistant_messages[-1][:50]}...")

            return " ".join(summary_parts)
        except Exception as e:
            Logger.warning(f"Could not generate context summary: {str(e)}")
            return ""

    async def store_context_snapshot(self, conversation_id: str, context_data: Dict[str, Any]) -> bool:
        """
        Store a snapshot of the current context

        Args:
            conversation_id: ID of the conversation
            context_data: Context data to store

        Returns:
            bool: True if stored successfully
        """
        try:
            # In this implementation, we're relying on the conversation service
            # to persist messages. For additional context snapshots, we could
            # implement additional storage mechanisms.

            # For now, we'll just log that a context snapshot was requested
            Logger.debug(f"Context snapshot stored for conversation {conversation_id}", extra={
                "snapshot_size": len(json.dumps(context_data)),
                "timestamp": __import__('datetime').datetime.now().isoformat()
            })

            return True
        except Exception as e:
            Logger.error(f"Error storing context snapshot: {str(e)}")
            return False

    async def get_context_size(self, conversation_id: str) -> int:
        """
        Get the size of the context in terms of messages

        Args:
            conversation_id: ID of the conversation

        Returns:
            int: Number of messages in the conversation
        """
        try:
            messages = await self.conversation_service.get_conversation_history(conversation_id)
            return len(messages)
        except Exception as e:
            Logger.error(f"Error getting context size: {str(e)}")
            return 0

    async def clear_context(self, conversation_id: str, keep_latest: int = 0) -> bool:
        """
        Clear context for a conversation, keeping only the latest messages

        Args:
            conversation_id: ID of the conversation
            keep_latest: Number of latest messages to keep (0 to remove all)

        Returns:
            bool: True if cleared successfully
        """
        try:
            # This would require a method in the conversation service to truncate history
            # For now, we'll just log the request
            Logger.info(f"Requested to clear context for conversation {conversation_id}, keeping {keep_latest} messages")

            # In a real implementation, this would remove older messages while keeping the latest N
            return True
        except Exception as e:
            Logger.error(f"Error clearing context: {str(e)}")
            return False

    def calculate_context_tokens(self, messages: List[Dict[str, str]]) -> int:
        """
        Calculate approximate token count for context

        Args:
            messages: List of messages to count tokens for

        Returns:
            int: Approximate token count
        """
        total_chars = 0
        for msg in messages:
            total_chars += len(msg.get("content", ""))

        # Rough estimate: 1 token ~ 4 characters
        return total_chars // 4

    async def is_context_size_acceptable(self, conversation_id: str, additional_tokens: int = 0) -> bool:
        """
        Check if adding more content would exceed token limits

        Args:
            conversation_id: ID of the conversation
            additional_tokens: Additional tokens to be added

        Returns:
            bool: True if context size is acceptable
        """
        try:
            messages = await self.conversation_service.get_conversation_history(conversation_id)

            context_messages = [
                {
                    "role": msg.role,
                    "content": msg.content
                } for msg in messages
            ]

            current_tokens = self.calculate_context_tokens(context_messages)
            return (current_tokens + additional_tokens) <= self.max_context_tokens
        except Exception as e:
            Logger.error(f"Error checking context size: {str(e)}")
            return False  # Be conservative on error