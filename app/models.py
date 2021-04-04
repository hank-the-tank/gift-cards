import datetime

import sqlalchemy as sa

from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL
from app.database import Base


class Order(Base):
    __tablename__ = "order"
    # create a ufnction for generating uuid
    id = sa.Column(
        GUID, primary_key=True, server_default=GUID_SERVER_DEFAULT_POSTGRESQL
    )
    created = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    code = sa.Column(sa.String)
    customer = sa.Column(sa.String)
