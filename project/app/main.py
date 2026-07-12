import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI

from app.api.health import router as health_router
from app.config.config import get_settings

from app.schemas.goals import GoalResponse, GoalCreate, GoalUpdate, DeleteGoal
from app.schemas.got_awards import CreateGot_Awards, ResponseGot_Awards
from app.schemas.awards import AwardsResponse, AwardsCreate
from app.schemas.friendship import FriendshipCreate, FriendshipDelete, FriendshipResponse
from app.schemas.profile import CreateProfile, UpdateProfile, ResponseProfile
from app.schemas.user import UserCreate, UserResponse, UserLogin


from app.database import Base, engine

from app.handlers.auth import router as auth_router
from app.handlers.goals import router as goals_router
from app.handlers.users import router as users_router
from app.handlers.profile import router as profile_router
from app.models.goal import Goal
from app.models.user import User

settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)

Base.metadata.create_all(bind=engine)
app.include_router(auth_router)
app.include_router(goals_router)
app.include_router(users_router)
app.include_router(health_router)
app.include_router(profile_router)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": f"{settings.app_name} is running"}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
