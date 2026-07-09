from fastapi import FastAPI

from app.api.health import router as health_router
from app.config.config import get_settings

from app.schemas.goals import goal
from app.schemas.got_awards import got_awards
from app.schemas.awards import awards
from app.schemas.friendship import friendship
from app.schemas.profile import profile
from app.schemas.user import user

from app.api.items import router as items_router

from app.database import Base, engine

Base.metadata.create_all(bind=engine)

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)

app.include_router(health_router)
app.include_router(items_router)

@app.get("/")
def root():
    return {
        "message": f"{settings.app_name} is running",
    }


@app.post("/user/register", response_model = user)
def register_user(user_data: user):
    return {"id": user_data.id, "password": user_data.password}

@app.get("/hello")
def hello():
    return {
        "message": "Hello, FastAPI!",
    }

@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {
        "item_id": item_id,
    }

@app.get("/search")
def search_items(query: str, limit: int = 10):
    return {
        "query": query,
        "limit": limit,
    }

@app.post("/items")
def create_item(item: ItemCreate):
    return {
        "message": "Item created",
        "item": item,
    }