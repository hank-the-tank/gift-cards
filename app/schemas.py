from pydantic import BaseModel
from datetime import datetime


class Order(BaseModel):
    customer: str
    code: str
    created: datetime