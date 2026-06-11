from pydantic import BaseModel


class ConversationCreate(BaseModel):
    user_id: int


class ConversationResponse(BaseModel):
    id: int
    user_id: int

    class Config:
        from_attributes = True