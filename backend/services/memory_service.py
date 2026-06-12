from sqlalchemy.orm import Session
from backend.models.message import Message
from backend.repositories.message_repository import MessageRepository


class MemoryService:

    @staticmethod
    def save_message(db: Session, conversation_id: int, role: str, content: str) -> Message:
        """
        Saves a single message to PostgreSQL.

        role: "user" or "assistant"
        content: actual message text
        """
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content
        )
        return MessageRepository.create(db, message)

    @staticmethod
    def get_history(db: Session, conversation_id: int, limit: int = 10) -> list[dict]:
        """
        Fetches last N messages of a conversation.
        Returns list of dicts with role and content.

        limit: how many recent messages to fetch (default 10)
        """
        messages = MessageRepository.get_by_conversation(
            db=db,
            conversation_id=conversation_id,
            limit=limit
        )

        # Convert to list of dicts for easy use
        return [
            {
                "role": message.role,
                "content": message.content
            }
            for message in messages
        ]

    @staticmethod
    def clear_history(db: Session, conversation_id: int) -> dict:
        """
        Deletes all messages of a conversation.
        """
        deleted_count = MessageRepository.delete_by_conversation(
            db=db,
            conversation_id=conversation_id
        )

        return {
            "status": "success",
            "deleted_messages": deleted_count
        }