import datetime

import sqlalchemy as sa

from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL
from app.database import Base


class Order(Base):
    __tablename__ = "order"

    id = sa.Column(
        GUID, primary_key=True, server_default=GUID_SERVER_DEFAULT_POSTGRESQL
    )
    created = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    code = sa.Column(sa.String)
    customer = sa.Column(sa.String)


class User(Base):
    __tablename__ = "user"

    id = sa.Column(
        GUID, primary_key=True, server_default=GUID_SERVER_DEFAULT_POSTGRESQL
    )
    created = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    name = sa.Column(sa.String)
    email = sa.Column(sa.String)
    password = sa.Column(sa.String)
