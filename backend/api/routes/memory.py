from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.services.memory_service import MemoryService

router = APIRouter()


@router.post("/{conversation_id}/messages")
def save_message(conversation_id: int, role: str, content: str, db: Session = Depends(get_db)):
    """
    Save a message to a conversation.
    role: 'user' or 'assistant'
    """
    result = MemoryService.save_message(
        db=db,
        conversation_id=conversation_id,
        role=role,
        content=content
    )
    return {"status": "success", "message_id": result.id}


@router.get("/{conversation_id}/messages")
def get_history(conversation_id: int, limit: int = 10, db: Session = Depends(get_db)):
    """
    Get last N messages of a conversation.
    """
    history = MemoryService.get_history(
        db=db,
        conversation_id=conversation_id,
        limit=limit
    )
    return {"conversation_id": conversation_id, "history": history}


@router.delete("/{conversation_id}/messages")
def clear_history(conversation_id: int, db: Session = Depends(get_db)):
    """
    Delete all messages of a conversation.
    """
    result = MemoryService.clear_history(
        db=db,
        conversation_id=conversation_id
    )
    return result