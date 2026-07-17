from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserLogin
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", status_code=201)
def register(schema: UserCreate, db: Session = Depends(get_db)):
    service = AuthService(db)
    service.register(schema)
    return {"message": "User created successfully"}

@router.post("/login")
def login(schema: UserLogin, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.login(schema)