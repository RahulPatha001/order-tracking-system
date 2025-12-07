from pydantic import BaseModel
import datetime

class order(BaseModel):
    id: int
    user_id: int
    status: str
    created_at: datetime
    updated_at: datetime
    