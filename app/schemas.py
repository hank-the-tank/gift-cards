from pydantic import BaseModel
from datetime import datetime


class OrderType(BaseModel):
    customer: str
    code: str
    created: datetime