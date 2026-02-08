"""
Orchestrator agent for the AI Agent Platform
Implements the core orchestrator functionality that routes requests to appropriate agents
"""
from typing import Dict, Any, Optional, List
from ..models.message import MessageCreate
from ..services.conversation_service import ConversationService
from ..skills.intent_analysis import IntentAnalysisSkill
from ..skills.response_formatting import ResponseFormattingSkill
from ..skills.error_handling import ErrorHandlingSkill
from .base_agent import BaseAgent, AgentResponse
from ..utils.logging import log_agent_decision, Logger
import asyncio
import re


class OrchestratorAgent(BaseAgent):
    """
    The orchestrator agent is responsible for:
    1. Analyzing user intent
    2. Selecting the appropriate specialized agent
    3. Coordinating between different agents and skills
    4. Ensuring proper flow of the conversation
    """

    def __init__(self, conversation_service: ConversationService):
        super().__init__(conversation_service)

        # Initialize skills
        self.intent_analysis_skill = IntentAnalysisSkill()
        self.response_formatting_skill = ResponseFormattingSkill()
        self.error_handling_skill = ErrorHandlingSkill()

        # Agent registry - maps intents to specialized agents
        self.agent_registry = {}
        
        # Define task-related intents for direct routing
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

    def register_agent(self, intent_keyword: str, agent: BaseAgent):
        """
        Register a specialized agent for a specific intent

        Args:
            intent_keyword: Keyword that triggers this agent
            agent: The specialized agent instance
        """
        self.agent_registry[intent_keyword.lower()] = agent

    def get_agent_type(self) -> str:
        """Return the type of agent"""
        return "orchestrator"

    async def process(self, message: str, conversation_id: str, user_id: str) -> AgentResponse:
        """
        Process a user message by orchestrating to the appropriate specialized agent

        Args:
            message: The user's input message
            conversation_id: ID of the conversation
            user_id: ID of the user

        Returns:
            AgentResponse: The agent's response with metadata
        """
        try:
            # Log the incoming request
            Logger.info(f"Orchestrator processing message: {message[:50]}...",
                       extra={"conversation_id": conversation_id, "user_id": user_id})

            # Check if this is a task-related request first
            task_intent = self._detect_task_intent(message)
            
            if task_intent:
                # Import the task management agent here to avoid circular imports
                from .task_management_agent import TaskManagementAgent
                from ..providers.gemini_adapter import GeminiProvider
                # Handle the import differently to avoid relative import issues
                import sys
                import os
                sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

                # Now import using the absolute path
                try:
                    from settings import settings
                except ImportError:
                    # If direct import fails, try with backend prefix
                    from backend.settings import settings
                
                # Initialize provider based on configuration
                if settings.llm_provider == "gemini":
                    if not settings.gemini_api_key:
                        raise ValueError("Gemini API key not configured")
                    provider = GeminiProvider(api_key=settings.gemini_api_key)
                else:
                    # Default to Gemini if provider not recognized
                    if not settings.gemini_api_key:
                        raise ValueError("Default provider API key not configured")
                    provider = GeminiProvider(api_key=settings.gemini_api_key)

                # Validate provider configuration
                if not provider.validate_config():
                    raise ValueError("Provider configuration validation failed - check API key and model access")

                # Create a task management agent
                task_agent = TaskManagementAgent(self.conversation_service, provider)
                
                # Process the task request directly
                response = await task_agent.process(message, conversation_id, user_id)
                
                return response

            # If not a task-related request, use the original intent analysis
            # Analyze intent using the intent analysis skill
            intent_result = await self.intent_analysis_skill.execute({"message": message})

            if not intent_result.success:
                Logger.error(f"Intent analysis failed: {intent_result.error}")
                return AgentResponse(
                    content="I'm sorry, I couldn't understand your request.",
                    error=intent_result.error
                )

            # Extract the determined intent
            detected_intent = intent_result.data.get("detected_intent", "general")
            confidence = intent_result.data.get("confidence", 0.0)

            # Log the intent decision
            log_agent_decision(
                agent_type=self.get_agent_type(),
                decision=f"Detected intent: {detected_intent}",
                confidence=confidence
            )

            # Route to appropriate agent based on intent
            if detected_intent in self.agent_registry:
                # Use the registered specialized agent
                specialized_agent = self.agent_registry[detected_intent]
                response = await specialized_agent.process(message, conversation_id, user_id)

                # Format the response using the formatting skill
                formatted_content = await self._format_response(response.content, detected_intent)

                return AgentResponse(
                    content=formatted_content,
                    metadata={
                        "source_agent": specialized_agent.get_agent_type(),
                        "detected_intent": detected_intent,
                        "confidence": confidence,
                        "orchestrated": True
                    }
                )
            else:
                # If no specific agent is registered for this intent,
                # default to general conversation handling
                Logger.info(f"No specific agent for intent '{detected_intent}', using default conversation handling")

                # For now, return a response indicating the intent was detected
                # In a full implementation, we'd have a default conversation agent
                formatted_content = await self._format_response(
                    f"I understand you're asking about '{detected_intent}'. How can I help you with this?",
                    detected_intent
                )

                return AgentResponse(
                    content=formatted_content,
                    metadata={
                        "detected_intent": detected_intent,
                        "confidence": confidence,
                        "orchestrated": False
                    }
                )

        except Exception as e:
            Logger.error(f"Error in orchestrator agent: {str(e)}", extra={"user_id": user_id})
            # Use error handling skill to format the error response
            error_result = await self.error_handling_skill.execute({"error": str(e)})

            return AgentResponse(
                content=error_result.data.get("message", f"I'm experiencing some difficulties. Error: {str(e)}"),
                error=str(e),
                metadata={"error_handled": True}
            )

    def _detect_task_intent(self, message: str) -> Optional[str]:
        """
        Detect if the message is related to task management

        Args:
            message: The user's message

        Returns:
            str or None: The detected intent or None if not a task-related message
        """
        message_lower = message.lower()
        
        for intent, patterns in self.task_intents.items():
            for pattern in patterns:
                if re.search(pattern, message_lower):
                    return intent
        
        return None

    async def _format_response(self, content: str, intent: str) -> str:
        """
        Format the response using the response formatting skill

        Args:
            content: Raw response content
            intent: The intent that triggered this response

        Returns:
            str: Formatted response content
        """
        formatting_result = await self.response_formatting_skill.execute({
            "content": content,
            "intent": intent
        })

        if formatting_result.success:
            return formatting_result.data.get("formatted_content", content)
        else:
            # If formatting fails, return the original content
            Logger.warning(f"Response formatting failed: {formatting_result.error}")
            return content

    async def add_message_to_conversation(self, conversation_id: str, role: str, content: str):
        """
        Helper method to add a message to the conversation

        Args:
            conversation_id: ID of the conversation
            role: Role of the message sender (user, assistant, etc.)
            content: Content of the message
        """
        message_data = MessageCreate(role=role, content=content)
        await self.conversation_service.add_message_to_conversation(
            conversation_id, message_data
        )