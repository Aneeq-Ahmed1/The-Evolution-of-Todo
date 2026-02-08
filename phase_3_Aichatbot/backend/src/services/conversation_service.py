"""
Conversation service for the AI Agent Platform
Handles all conversation-related operations
"""
from typing import List, Optional, Union
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import NoResultFound
from datetime import datetime, timedelta
from ..models.conversation import Conversation, ConversationCreate, ConversationRead
from ..models.message import Message, MessageCreate, MessageRead
from ..models.skill_log import SkillExecutionLog, SkillExecutionLogCreate
from ..db.database import get_session
from ..db.settings import settings
import uuid
from uuid import UUID


class ConversationService:
    """Service class to handle all conversation operations"""

    def __init__(self, session: AsyncSession):
        """
        Initialize the conversation service

        Args:
            session: Database session
        """
        self.session = session

    async def create_conversation(self, user_id: str, title: Optional[str] = None) -> ConversationRead:
        """
        Create a new conversation

        Args:
            user_id: ID of the user creating the conversation
            title: Optional title for the conversation (will be auto-generated if not provided)

        Returns:
            ConversationRead: The created conversation
        """
        if not title:
            title = f"Conversation {datetime.now().strftime('%Y-%m-%d %H:%M')}"

        # Ensure user_id is a string (convert from UUID if needed)
        user_id_str = str(user_id) if isinstance(user_id, uuid.UUID) else user_id

        conversation = Conversation(
            user_id=user_id_str,
            title=title,
            metadata_json={}
        )
        self.session.add(conversation)
        await self.session.commit()
        await self.session.refresh(conversation)

        # For SQLModel 0.0.8 compatibility, use model_dump instead of dict() if available
        try:
            return ConversationRead.model_validate(conversation)
        except AttributeError:
            # Fallback for older versions
            if hasattr(ConversationRead, 'from_orm'):
                return ConversationRead.from_orm(conversation)
            else:
                return ConversationRead(**conversation.dict())

    async def get_conversation(self, conversation_id: Union[UUID, str]) -> Optional[ConversationRead]:
        """
        Get a conversation by ID

        Args:
            conversation_id: ID of the conversation

        Returns:
            ConversationRead: The conversation or None if not found
        """
        # Convert UUID to string if needed since the database stores IDs as strings
        conversation_id_str = str(conversation_id) if isinstance(conversation_id, UUID) else conversation_id
        conversation = await self.session.get(Conversation, conversation_id_str)
        if conversation:
            try:
                return ConversationRead.model_validate(conversation)
            except AttributeError:
                if hasattr(ConversationRead, 'from_orm'):
                    return ConversationRead.from_orm(conversation)
                else:
                    return ConversationRead(**conversation.dict())
        return None

    async def get_user_conversations(self, user_id: UUID) -> List[ConversationRead]:
        """
        Get all conversations for a user

        Args:
            user_id: ID of the user

        Returns:
            List[ConversationRead]: List of user's conversations
        """
        statement = select(Conversation).where(Conversation.user_id == user_id)
        results = await self.session.exec(statement)
        conversations = []
        for conv in results:
            try:
                conversations.append(ConversationRead.model_validate(conv))
            except AttributeError:
                if hasattr(ConversationRead, 'from_orm'):
                    conversations.append(ConversationRead.from_orm(conv))
                else:
                    conversations.append(ConversationRead(**conv.dict()))
        return conversations

    async def add_message_to_conversation(self, conversation_id: Union[UUID, str], message_data: MessageCreate) -> MessageRead:
        """
        Add a message to a conversation

        Args:
            conversation_id: ID of the conversation
            message_data: Data for the new message

        Returns:
            MessageRead: The created message
        """
        # Convert UUID to string if needed since the database stores IDs as strings
        conversation_id_str = str(conversation_id) if isinstance(conversation_id, UUID) else conversation_id
        
        message = Message(
            conversation_id=conversation_id_str,
            user_id=message_data.user_id,
            role=message_data.role,
            content=message_data.content,
            tool_calls=message_data.tool_calls,
            tool_response=message_data.tool_response,
            created_at=datetime.utcnow()  # Add required field
        )
        self.session.add(message)
        await self.session.commit()
        await self.session.refresh(message)

        try:
            return MessageRead.model_validate(message)
        except AttributeError:
            if hasattr(MessageRead, 'from_orm'):
                return MessageRead.from_orm(message)
            else:
                return MessageRead(**message.dict())

    async def get_conversation_history(self, conversation_id: Union[UUID, str], limit: int = 50) -> List[MessageRead]:
        """
        Get the message history for a conversation

        Args:
            conversation_id: ID of the conversation
            limit: Maximum number of messages to return (default 50, newest first)

        Returns:
            List[MessageRead]: List of messages in the conversation
        """
        # Convert UUID to string if needed since the database stores IDs as strings
        conversation_id_str = str(conversation_id) if isinstance(conversation_id, UUID) else conversation_id
        
        statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id_str)
            .order_by(Message.timestamp.desc())
            .limit(limit)
        )
        results = await self.session.exec(statement)
        messages = []
        for msg in results:
            try:
                messages.append(MessageRead.model_validate(msg))
            except AttributeError:
                if hasattr(MessageRead, 'from_orm'):
                    messages.append(MessageRead.from_orm(msg))
                else:
                    messages.append(MessageRead(**msg.dict()))
        return messages[::-1]  # Reverse to get chronological order (oldest first)

    async def get_messages_for_conversation(self, conversation_id: Union[UUID, str]) -> List[MessageRead]:
        """
        Get all messages for a conversation in chronological order

        Args:
            conversation_id: ID of the conversation

        Returns:
            List[MessageRead]: List of all messages in the conversation in chronological order
        """
        # Convert UUID to string if needed since the database stores IDs as strings
        conversation_id_str = str(conversation_id) if isinstance(conversation_id, UUID) else conversation_id
        
        statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id_str)
            .order_by(Message.timestamp.asc())  # Ascending order for chronological
        )
        results = await self.session.exec(statement)
        messages = []
        for msg in results:
            try:
                messages.append(MessageRead.model_validate(msg))
            except AttributeError:
                if hasattr(MessageRead, 'from_orm'):
                    messages.append(MessageRead.from_orm(msg))
                else:
                    messages.append(MessageRead(**msg.dict()))
        return messages

    async def update_conversation_title(self, conversation_id: Union[UUID, str], title: str) -> Optional[ConversationRead]:
        """
        Update the title of a conversation

        Args:
            conversation_id: ID of the conversation
            title: New title

        Returns:
            ConversationRead: Updated conversation or None if not found
        """
        # Convert UUID to string if needed since the database stores IDs as strings
        conversation_id_str = str(conversation_id) if isinstance(conversation_id, UUID) else conversation_id
        conversation = await self.session.get(Conversation, conversation_id_str)
        if conversation:
            conversation.title = title
            conversation.updated_at = datetime.utcnow()
            self.session.add(conversation)
            await self.session.commit()
            await self.session.refresh(conversation)

            try:
                return ConversationRead.model_validate(conversation)
            except AttributeError:
                if hasattr(ConversationRead, 'from_orm'):
                    return ConversationRead.from_orm(conversation)
                else:
                    return ConversationRead(**conversation.dict())
        return None

    async def delete_conversation(self, conversation_id: Union[UUID, str]) -> bool:
        """
        Delete a conversation and all its messages

        Args:
            conversation_id: ID of the conversation to delete

        Returns:
            bool: True if deleted, False if not found
        """
        # Convert UUID to string if needed since the database stores IDs as strings
        conversation_id_str = str(conversation_id) if isinstance(conversation_id, UUID) else conversation_id
        conversation = await self.session.get(Conversation, conversation_id_str)
        if conversation:
            # Delete all related messages first (due to foreign key constraints)
            message_statement = select(Message).where(Message.conversation_id == conversation_id_str)
            message_results = await self.session.exec(message_statement)
            messages = message_results.all()
            for msg in messages:
                self.session.delete(msg)

            # Delete the conversation
            self.session.delete(conversation)
            await self.session.commit()
            return True
        return False

    async def log_skill_execution(self, conversation_id: Union[UUID, str], skill_log_data: SkillExecutionLogCreate) -> bool:
        """
        Log a skill execution

        Args:
            conversation_id: ID of the conversation
            skill_log_data: Data for the skill execution log

        Returns:
            bool: True if logged successfully
        """
        # Convert UUID to string if needed since the database stores IDs as strings
        conversation_id_str = str(conversation_id) if isinstance(conversation_id, UUID) else conversation_id
        
        skill_log = SkillExecutionLog(
            conversation_id=conversation_id_str,
            skill_name=skill_log_data.skill_name,
            input_params=skill_log_data.input_params,
            output_result=skill_log_data.output_result,
            execution_time=skill_log_data.execution_time
        )
        self.session.add(skill_log)
        await self.session.commit()
        return True

    async def cleanup_expired_conversations(self) -> int:
        """
        Remove conversations that are older than the retention period

        Returns:
            int: Number of conversations deleted
        """
        retention_days = settings.conversation_retention_days
        cutoff_date = datetime.utcnow() - timedelta(days=retention_days)

        # Find conversations to delete
        statement = select(Conversation).where(Conversation.created_at < cutoff_date)
        result = await self.session.exec(statement)
        conversations_to_delete = result.all()

        count = 0
        for conversation in conversations_to_delete:
            await self.delete_conversation(conversation.id)
            count += 1

        return count