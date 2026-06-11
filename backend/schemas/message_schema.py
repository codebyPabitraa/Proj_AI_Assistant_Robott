from pydantic import BaseModel


class MessageCreate(BaseModel):
    conversation_id: int
    role: str
    content: str


class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    role: str
    content: str

    class Config:
        from_attributes = True