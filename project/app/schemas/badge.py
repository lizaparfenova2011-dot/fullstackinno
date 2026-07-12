from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional

class BadgeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: str
    image_url: str | None
    condition_type: str
    condition_params: dict

class UserBadgeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    badge_id: int
    awarded_at: datetime
    badge: BadgeResponse

class CountersResponse(BaseModel):
    day_count: int
    week_count: int
    month_count: int
    year_count: int