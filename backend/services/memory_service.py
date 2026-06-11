# Memory CRUD service
from sqlalchemy.orm import Session

from backend.repositories.conversation_repository import (
    ConversationRepository,
)
from backend.repositories.message_repository import (
    MessageRepository,
)


class MemoryService:

    @staticmethod
    def create_conversation(
        db: Session,
        user_id: int,
    ):
        return ConversationRepository.create(
            db=db,
            user_id=user_id,
        )

    @staticmethod
    def add_message(
        db: Session,
        conversation_id: int,
        role: str,
        content: str,
    ):
        return MessageRepository.create(
            db=db,
            conversation_id=conversation_id,
            role=role,
            content=content,
        )

    @staticmethod
    def get_conversation_history(
        db: Session,
        conversation_id: int,
    ):
        return MessageRepository.get_by_conversation(
            db=db,
            conversation_id=conversation_id,
        )