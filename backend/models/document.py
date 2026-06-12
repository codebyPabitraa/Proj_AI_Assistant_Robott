from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.database.base import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, nullable=True)

    filename = Column(String(255), nullable=False)

    file_type = Column(String(50), nullable=False)

    file_size = Column(Integer, nullable=True)

    word_count = Column(Integer, nullable=True)

    chunk_count = Column(Integer, nullable=True)

    collection_name = Column(String(100), nullable=True)

    doc_id = Column(String(255), nullable=True)

    status = Column(String(50), default="success")

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )