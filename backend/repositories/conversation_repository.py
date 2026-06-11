from sqlalchemy.orm import Session

from backend.models.conversation import Conversation


class ConversationRepository:

    @staticmethod
    def create(db: Session, user_id: int) -> Conversation:
        conversation = Conversation(
            user_id=user_id
        )

        db.add(conversation)
        db.commit()
        db.refresh(conversation)

        return conversation

    @staticmethod
    def get_by_id(db: Session, conversation_id: int):
        return (
            db.query(Conversation)
            .filter(Conversation.id == conversation_id)
            .first()
        )