from pydantic import BaseModel, Field, Json
from datetime import datetime, time
from typing import Optional, Literal, Dict

class order_dto(BaseModel):
    user_id: str
    currency:str = 'INR'
    mode: str = 'web'
    items: Dict[str, int]
    price: int
    