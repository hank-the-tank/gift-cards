import datetime

import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL
from app.database import Base, Session


class Customer(Base):
    __tablename__ = "customer"

    id = sa.Column(
        GUID, primary_key=True, server_default=GUID_SERVER_DEFAULT_POSTGRESQL
    )
    created = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    name = sa.Column(sa.String)
    email = sa.Column(sa.String)
    password = sa.Column(sa.String)

    orders = relationship("Order", back_populates="customer")


class Order(Base):
    __tablename__ = "order"

    id = sa.Column(
        GUID, primary_key=True, server_default=GUID_SERVER_DEFAULT_POSTGRESQL
    )
    created = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    code = sa.Column(sa.String)

    customer_id = sa.Column(GUID, ForeignKey("customer.id"))
    customer = relationship("Customer", back_populates="orders")


class User(Base):
    __tablename__ = "user"

    id = sa.Column(
        GUID, primary_key=True, server_default=GUID_SERVER_DEFAULT_POSTGRESQL
    )
    created = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    name = sa.Column(sa.String, nullable=True)
    email = sa.Column(sa.String, nullable=False)
    password = sa.Column(sa.String, nullable=False)
