from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.session import get_db
from backend.services.memory_service import MemoryService

from backend.schemas.conversation_schema import (
    ConversationCreate,
    ConversationResponse,
)

from backend.schemas.message_schema import (
    MessageCreate,
    MessageResponse,
)

router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)


@router.post("/", response_model=ConversationResponse)
def create_conversation(
    conversation: ConversationCreate,
    db: Session = Depends(get_db),
):
    return MemoryService.create_conversation(
        db=db,
        user_id=conversation.user_id,
    )


@router.post("/messages", response_model=MessageResponse)
def add_message(
    message: MessageCreate,
    db: Session = Depends(get_db),
):
    return MemoryService.add_message(
        db=db,
        conversation_id=message.conversation_id,
        role=message.role,
        content=message.content,
    )


@router.get("/{conversation_id}/messages")
def get_history(
    conversation_id: int,
    db: Session = Depends(get_db),
):
    return MemoryService.get_conversation_history(
        db=db,
        conversation_id=conversation_id,
    )