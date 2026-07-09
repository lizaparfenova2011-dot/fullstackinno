from pydantic import BaseModel

class friendship(BaseModel):
    id: int
    name: text
    sender_id: int
    recipient_id: int