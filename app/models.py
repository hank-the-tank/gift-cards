import datetime

from sqlalchemy import Column, DateTime, String

from app.database import Base
from uuid import uuid4


class Order(Base):
    __tablename__ = "order"

    id = Column(String, primary_key=True, default=uuid4())
    created = Column(DateTime, default=datetime.datetime.utcnow)
    customer = Column(String)
