import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI

from app.api.health import router as health_router
from app.config.config import get_settings

from app.schemas.goals import GoalResponse, GoalCreate, GoalUpdate, DeleteGoal
from app.schemas.profile import ProfileUpdate, ProfileResponse
from app.schemas.user import UserCreate, UserResponse, UserLogin


from app.database import Base, engine

from app.handlers.auth import router as auth_router
from app.handlers.goals import router as goals_router
from app.handlers.users import router as users_router
from app.handlers.profile import router as profile_router
from app.handlers.badges import router as badges_router
from app.models.goal import Goal
from app.models.user import User
from fastapi.middleware.cors import CORSMiddleware
from app.models.badge import Badge, UserBadge
from app.models.user_counter import UserCounter

settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
from app.database import SessionLocal
from app.models.badge import Badge

def seed_badges():
    db = SessionLocal()
    try:
        db.query(Badge).delete()
        db.commit()

        predefined = [
            {"name": "Деревянная монетка", "description": "(Выполните 15 целей на день)  Начинающий пользователь", "condition_type": "period_count", "condition_params": {"period": "day", "count": 15}, "image_url": "wood.png"},
            {"name": "Алюминиевая монетка", "description": "(Выполните 5 целей на неделю)  Труженник", "condition_type": "period_count", "condition_params": {"period": "week", "count": 5}, "image_url": "aluminium.png"},
            {"name": "Бронзовая монетка", "description": "(Выполните 15 целей на неделю)  Упорный", "condition_type": "period_count", "condition_params": {"period": "week", "count": 15}, "image_url": "bronze.png"},
            {"name": "Аметистовая монетка", "description": "(Выполните 10 целей на месяц)  Труд его боялся", "condition_type": "period_count", "condition_params": {"period": "month", "count": 10}, "image_url": "ametist.png"},
            {"name": "Серебряная монетка", "description": "(Выполните 15 целей на месяц)  Суперумница", "condition_type": "period_count", "condition_params": {"period": "month", "count": 15}, "image_url": "serebro.png"},
            {"name": "Изумрудная монетка", "description": "(Выполните 30 целей на месяц)  Целеустремлённый", "condition_type": "period_count", "condition_params": {"period": "month", "count": 30}, "image_url": "izumrud.png"},
            {"name": "Сапфировая монетка", "description": "(Выполните 50 целей на месяц)  Молодчина", "condition_type": "period_count", "condition_params": {"period": "month", "count": 50}, "image_url": "sapfir.png"},
            {"name": "Монетка из розового кварца", "description": "(Выполните 5 целей на год)  Трудоголик", "condition_type": "period_count", "condition_params": {"period": "year", "count": 5}, "image_url": "pink.png"},
            {"name": "Рубиновая монетка", "description": "(Выполните 25 целей на год)  Трудолюбивчик", "condition_type": "period_count", "condition_params": {"period": "year", "count": 25}, "image_url": "rubin.png"},
            {"name": "Золотая монетка", "description": "(Выполните 50 целей на год)  Работяга", "condition_type": "period_count", "condition_params": {"period": "year", "count": 50}, "image_url": "gold.png"},
            {"name": "Алмазная монетка", "description": "(Выполните 67 целей на год)  Неостанавливаемый", "condition_type": "period_count", "condition_params": {"period": "year", "count": 67}, "image_url": "almaz.png"},
            {"name": "Хрустальная монетка", "description": "(Выполните 100 целей на год)  Великий трудяга", "condition_type": "period_count", "condition_params": {"period": "year", "count": 100}, "image_url": "chrustal.png"},
        ]
        for data in predefined:
            badge = Badge(**data)
            db.add(badge)
        db.commit()
    finally:
        db.close()

seed_badges()
app.include_router(auth_router)
app.include_router(goals_router)
app.include_router(users_router)
app.include_router(health_router)
app.include_router(profile_router)
app.include_router(badges_router)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": f"{settings.app_name} is running"}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
