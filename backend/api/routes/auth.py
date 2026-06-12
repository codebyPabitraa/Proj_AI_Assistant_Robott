from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
from backend.database.session import get_db
from backend.services.auth_service import AuthService
from backend.api.dependencies import get_current_user
from backend.models.user import User

router = APIRouter()


# --- Register Schema ---
class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str


# --- Register Endpoint ---
@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """
    Register a new user.
    Hashes password and stores in PostgreSQL.
    """
    try:
        user = AuthService.register(
            db=db,
            name=request.name,
            email=request.email,
            password=request.password
        )
        return {
            "status": "success",
            "user_id": user.id,
            "name": user.name,
            "email": user.email
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# --- Login Endpoint ---
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login with email and password.
    Returns JWT token.
    """
    try:
        token = AuthService.login(
            db=db,
            email=form_data.username,
            password=form_data.password
        )
        return {
            "access_token": token,
            "token_type": "bearer"
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


# --- Get Current User Endpoint ---
@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    """
    Returns currently logged in user.
    Protected route — requires valid token.
    """
    return {
        "user_id": current_user.id,
        "name": current_user.name,
        "email": current_user.email
    }