from sqlalchemy.orm import Session

from backend.models.message import Message


class MessageRepository:

    @staticmethod
    def create(
        db: Session,
        conversation_id: int,
        role: str,
        content: str
    ) -> Message:

        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content
        )

        db.add(message)
        db.commit()
        db.refresh(message)

        return message

    @staticmethod
    def get_by_conversation(
        db: Session,
        conversation_id: int
    ):
        return (
            db.query(Message)
            .filter(
                Message.conversation_id == conversation_id
            )
            .all()
        )