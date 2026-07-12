from pydantic import BaseModel, Field, ConfigDict

class AwardsCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)

class AwardsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    png_url: str
    for_what: str