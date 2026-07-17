from enum import Enum
from sqlalchemy import Boolean, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from datetime import datetime

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    role: Mapped[str] = mapped_column(String(50), default=UserRole.USER.value, nullable=False)

    # Поля профиля (добавлены ранее)
    name: Mapped[str | None] = mapped_column(String(100), nullable=True, default=None)
    avatar_url: Mapped[str | None] = mapped_column(String(300), nullable=True, default=None)
    theme: Mapped[str] = mapped_column(String(20), nullable=False, default="system")

    # Связь с наградами (можно оставить, если была)
    badges = relationship("UserBadge", back_populates="user")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)