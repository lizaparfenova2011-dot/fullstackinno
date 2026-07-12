from pydantic import BaseModel, Field, ConfigDict

class FriendshipCreate(BaseModel):
    request: bool = False
    name: str = Field(min_length=1, max_length=200)
    accept: bool = False

class FriendshipResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    sender_id: int
    recipient_id: int
    accept: bool

class FriendshipDelete(BaseModel):
    message: str
    deleted_goal_id: int