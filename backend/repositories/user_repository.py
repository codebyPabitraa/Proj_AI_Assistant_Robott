from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from backend.models.user import User


class UserRepository:

    @staticmethod
    def create(db: Session, name: str, email: str) -> User:
        user = User(
            name=name,
            email=email
        )

        try:
            db.add(user)
            db.commit()
            db.refresh(user)
            return user

        except IntegrityError:
            db.rollback()
            raise

    @staticmethod
    def get_all(db: Session):
        return db.query(User).all()