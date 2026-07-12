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
        if db.query(Badge).count() == 0:
            predefined = [
                # День
                {"name": "Деревянная монетка", "description": "Начинающий пользователь", "condition_type": "period_count", "condition_params": {"period": "day", "count": 15}},
                # Неделя
                {"name": "Алюминиевая монетка", "description": "Труженник", "condition_type": "period_count", "condition_params": {"period": "week", "count": 5}},
                {"name": "Бронзовая", "description": "Упорный", "condition_type": "period_count", "condition_params": {"period": "week", "count": 15}},
                # Месяц
                {"name": "Аметистовая", "description": "Труд его боялся", "condition_type": "period_count", "condition_params": {"period": "month", "count": 10}},
                {"name": "Серебрянная", "description": "Суперумница", "condition_type": "period_count", "condition_params": {"period": "month", "count": 15}},
                {"name": "Изумрудная", "description": "Целеустремлённый", "condition_type": "period_count", "condition_params": {"period": "month", "count": 30}},
                {"name": "Сапфировая", "description": "Молодчина", "condition_type": "period_count", "condition_params": {"period": "month", "count": 50}},
                # Год
                {"name": "Розовый кварц", "description": "Трудоголик", "condition_type": "period_count", "condition_params": {"period": "year", "count": 5}},
                {"name": "Рубиновая", "description": "Трудолюбивчик", "condition_type": "period_count", "condition_params": {"period": "year", "count": 25}},
                {"name": "Золотая", "description": "Работяга", "condition_type": "period_count", "condition_params": {"period": "year", "count": 50}},
                {"name": "Алмазная", "description": "Неостанавливаемый", "condition_type": "period_count", "condition_params": {"period": "year", "count": 67}},
                {"name": "Хрустальная", "description": "Великий трудяга", "condition_type": "period_count", "condition_params": {"period": "year", "count": 100}},
            ]
            for data in predefined:
                badge = Badge(**data)
                db.add(badge)
            db.commit()
    finally:
        db.close()

# после create_all
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
