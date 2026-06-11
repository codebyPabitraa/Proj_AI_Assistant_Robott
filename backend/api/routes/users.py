from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from backend.database.session import get_db
from backend.schemas.user_schema import UserCreate, UserResponse
from backend.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return UserService.create_user(
            db=db,
            name=user.name,
            email=user.email,
        )
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Email already exists."
        )

@router.get("/", response_model=list[UserResponse])
def get_users(
    db: Session = Depends(get_db)
):
    return UserService.get_users(db)