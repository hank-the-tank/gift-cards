from typing import List

import uvicorn
from fastapi import FastAPI
from sqlalchemy import select

from app.models import Order

from app.database import engine, Session
from app import models
from app.schemas import OrderType

models.Base.metadata.create_all(engine)
app = FastAPI()
session = Session()


@app.get('/')
def index():
    return dict(data="hello world")


@app.get('/order/{id}')
def view_order(id: str):
    return dict(data=id)


@app.get('/orders')
def view_orders():
    orders: List[Order] = session.query(Order).all()

    return dict(data=orders)
#


@app.post('/order')
def create_order(request: OrderType):
    return dict(data=Order)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8001)