from pydantic import BaseModel

class got_awards(BaseModel):
    id: int
    user_id: int
    award_id: int
    date_of_receiving: date