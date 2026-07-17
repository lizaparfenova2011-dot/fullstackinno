from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import datetime

class UserCreate(BaseModel):
    email: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=6, max_length=128)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        v = v.strip().lower()
        if "@" not in v:
            raise ValueError("Email must contain @")
        return v

class UserLogin(BaseModel):
    email: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=1, max_length=128)

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: str
    is_active: bool
    role: str
    name: str | None = None
    avatar_url: str | None = None
    theme: str = "system"
    created_at: datetime