from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter(
    prefix="/items",
    tags=["items"],
)


class ItemCreate(BaseModel):
    title: str
    description: str | None = None
    price: float


@router.get("")
def get_items():
    return [
        {
            "id": 1,
            "title": "Keyboard",
            "price": 5000,
        }
    ]


@router.post("")
def create_item(item: ItemCreate):
    return {
        "message": "Item created",
        "item": item,
    }