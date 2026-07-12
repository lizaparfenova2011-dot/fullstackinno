from pydantic import BaseModel, Field, ConfigDict
from datetime import date

class CreateGot_Awards(BaseModel):
    name: str = Field(min_length=1, max_length=200)

class ResponseGot_Awards(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    award_id: int
    date_of_receiving: date