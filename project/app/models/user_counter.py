from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class UserCounter(Base):
    __tablename__ = "user_counters"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    period: Mapped[str] = mapped_column(String(10), nullable=False)   # "day", "week", "month", "year"
    count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)