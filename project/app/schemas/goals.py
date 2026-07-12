from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class GoalCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    period: str = Field(min_length=1, max_length=20)
    is_pinned: bool = False

class GoalUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    period: Optional[str] = Field(default=None, min_length=1, max_length=20)
    is_pinned: Optional[bool] = None
    is_completed: Optional[bool] = None

class GoalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    name: str
    is_pinned: bool
    period: str
    is_completed: bool
    created_at: date
    completed_at: date | None

class DeleteGoal(BaseModel):
    message: str
    deleted_goal_id: int

class DeleteByPeriodRequest(BaseModel):
    period: str = Field(..., min_length=1, max_length=20)

class ToggleCompletedResponse(BaseModel):
    goal_id: int
    is_completed: bool
    message: str

class TogglePinnedResponse(BaseModel):
    goal_id: int
    is_pinned: bool
    message: str