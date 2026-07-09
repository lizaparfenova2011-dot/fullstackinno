from pydantic import BaseModel

class awards(BaseModel):
    id: int
    name: text
    png_url: text
    for_what: text