from datetime import date
from sqlalchemy import String, Boolean, Date, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Goal(Base):
    __tablename__ = "goals"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    is_pinned: Mapped[bool] = mapped_column(Boolean, default=False)
    period: Mapped[str] = mapped_column(String, nullable=False)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[date] = mapped_column(Date, nullable=False)
    completed_at: Mapped[date | None] = mapped_column(Date, nullable=True)
