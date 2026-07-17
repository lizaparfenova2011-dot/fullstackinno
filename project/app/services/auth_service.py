from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.auth import hash_password, verify_password, create_access_token
from app.schemas.user import UserCreate, UserLogin
from datetime import datetime

class AuthService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def register(self, schema: UserCreate) -> User:
        existing = self.repository.get_by_email(schema.email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        user = User(
            email=schema.email,
            hashed_password=hash_password(schema.password),
            name=None,
            avatar_url=None,
            theme="system",
            created_at=datetime.utcnow() 
        )
        return self.repository.create(user)

    def login(self, schema: UserLogin) -> dict:
        user = self.repository.get_by_email(schema.email)
        if not user or not verify_password(schema.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        token = create_access_token(user.id)
        return {"access_token": token, "token_type": "bearer"}