from sqlalchemy.orm import Session
from backend.models.message import Message


class MessageRepository:

    @staticmethod
    def create(db: Session, message: Message) -> Message:
        """
        Saves a Message object to PostgreSQL.
        """
        db.add(message)
        db.commit()
        db.refresh(message)
        return message

    @staticmethod
    def get_by_conversation(db: Session, conversation_id: int, limit: int = 10) -> list[Message]:
        """
        Fetches last N messages of a conversation ordered by time.
        """
        return (
            db.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def delete_by_conversation(db: Session, conversation_id: int) -> int:
        """
        Deletes all messages of a conversation.
        Returns count of deleted messages.
        """
        deleted_count = (
            db.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .delete()
        )
        db.commit()
        return deleted_count