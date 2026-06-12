from sqlalchemy.orm import Session
from backend.models.document import Document


class DocumentRepository:

    @staticmethod
    def create(db: Session, document: Document) -> Document:
        db.add(document)
        db.commit()
        db.refresh(document)
        return document

    @staticmethod
    def get_all(db: Session) -> list[Document]:
        return db.query(Document).order_by(Document.created_at.desc()).all()

    @staticmethod
    def get_by_id(db: Session, document_id: int) -> Document:
        return db.query(Document).filter(Document.id == document_id).first()

    @staticmethod
    def get_by_user(db: Session, user_id: int) -> list[Document]:
        return db.query(Document).filter(
            Document.user_id == user_id
        ).order_by(Document.created_at.desc()).all()

    @staticmethod
    def delete(db: Session, document_id: int) -> bool:
        document = db.query(Document).filter(Document.id == document_id).first()
        if document:
            db.delete(document)
            db.commit()
            return True
        return False