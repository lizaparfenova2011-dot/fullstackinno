from pydantic import BaseModel

class profile(BaseModel):
    id: int
    user_id: int
    name: text
    avatar_url: text
    theme: text
    reg_date: date