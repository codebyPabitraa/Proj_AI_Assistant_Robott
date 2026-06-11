from sqlalchemy.orm import Session

from backend.repositories.user_repository import UserRepository


class UserService:

    @staticmethod
    def create_user(db: Session, name: str, email: str):
        return UserRepository.create(
            db=db,
            name=name,
            email=email
        )

    @staticmethod
    def get_users(db: Session):
        return UserRepository.get_all(db)