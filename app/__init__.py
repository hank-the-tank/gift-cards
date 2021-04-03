import uvicorn
from fastapi import FastAPI

from app.schemas import Order
from app.database import engine
from app import models


models.Base.metadata.create_all(engine)
app = FastAPI()


@app.get('/')
def index():
    return dict(data="hello world")

@app.get('/order/{id}')
def order(id: str):
    return dict(data=id)


@app.post('/order')
def create_order(request: Order):
    return dict(data=Order)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8001)