import datetime

from sqlalchemy import Column, DateTime, String

from app.database import Base
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID


class Order(Base):
    __tablename__ = "order"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4())
    created = Column(DateTime, default=datetime.datetime.utcnow)
    code = Column(String)
    customer = Column(String)
