from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from datetime import datetime

class ThemeEnum(str, Enum):
    SYSTEM = "system"
    LIGHT = "light"
    DARK = "dark"
    FOREST = "forest"
    OCEAN = "ocean"
    SUNSET = "sunset"

class ProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: str
    name: str | None
    avatar_url: str | None
    theme: str
    role: str
    created_at: datetime | None = None

class ProfileUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    avatar_url: Optional[str] = Field(default=None, min_length=1, max_length=300)
    theme: Optional[ThemeEnum] = None   # ← теперь тема принимается только из списка

class PasswordChange(BaseModel):
    old_password: str = Field(min_length=1, max_length=128)
    new_password: str = Field(min_length=6, max_length=128)