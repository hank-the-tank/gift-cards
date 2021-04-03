from typing import List

import uvicorn
from fastapi import FastAPI, Depends
from app import models as m

from app.database import engine, Session
from app import models, schemas

models.Base.metadata.create_all(engine)
app = FastAPI()


def db_connection():
    session = Session()
    try:
        yield session
    finally:
        session.close()


@app.get("/")
def index():
    return dict(data="landing page")


@app.get("/order/{id}")
def view_order(id: str, db: Session = Depends(db_connection)):
    order: m.Order = db.query(m.Order).filter_by(id=id).first()
    return dict(data=order)


@app.get("/orders")
def view_orders(db: Session = Depends(db_connection)):
    orders: List[m.Order] = db.query(m.Order).all()

    return dict(data=orders)


@app.post("/order")
def create_order(request: schemas.OrderType, db: Session = Depends(db_connection)):
    new_order: m.Order = m.Order(customer=request.customer, code=request.code)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
