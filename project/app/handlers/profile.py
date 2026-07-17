from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.profile import ProfileResponse, ProfileUpdate, PasswordChange
from app.services.user_service import UserService
from app.auth import get_current_user

router = APIRouter(prefix="/profile", tags=["profile"])

@router.get("/", response_model=ProfileResponse)
def get_profile(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = UserService(db)
    return service.get_profile(current_user.id)

@router.patch("/", response_model=ProfileResponse)
def update_profile(
    profile_data: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = UserService(db)
    return service.update_profile(current_user.id, profile_data)

@router.patch("/password", response_model=dict)
def change_password(
    passwords: PasswordChange,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = UserService(db)
    return service.change_password(current_user.id, passwords)