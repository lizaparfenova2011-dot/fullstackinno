from pydantic import BaseModel

class ItemCreate(BaseModel):
    title: str
    description: str | None = None
    price: float

class goal(BaseModel):
    id: int
    user_id: int
    name: text
    is_pinned: bool
    length: text
    is_competed: bool
    create_date: date
    complete_date: date
    process: int
    attach_to_id: int
