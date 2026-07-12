from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.schemas.profile import ProfileUpdate, PasswordChange

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from app.auth import hash_password
from app.models.user import User, UserRole
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class UserService:

    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def create_user(self, schema: UserCreate) -> User:
        existing_user = self.repository.get_by_email(schema.email)

        if existing_user is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists",
            )

        user = User(
            email=schema.email,
            hashed_password=hash_password(schema.password),
            is_active=True,
            role=UserRole.USER.value,
        )

        return self.repository.create(user)

    def get_users(self) -> list[User]:
        return self.repository.get_all()

    def get_user(self, user_id: int) -> User:
        user = self.repository.get_by_id(user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return user
    
    def get_profile(self, user_id: int) -> User:
        user = self.repository.get_by_id(user_id)  # предполагаю, что такой метод есть
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def update_profile(self, user_id: int, data: ProfileUpdate) -> User:
        user = self.get_profile(user_id)
        update_dict = data.model_dump(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(user, field, value)
        self.repository.update(user)
        return user

    def change_password(self, user_id: int, passwords: PasswordChange) -> dict:
        user = self.get_profile(user_id)
        if not pwd_context.verify(passwords.old_password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Old password is incorrect")
        # хешируем новый и сохраняем
        user.hashed_password = pwd_context.hash(passwords.new_password)
        self.repository.update(user)
        return {"message": "Password changed successfully"}
    