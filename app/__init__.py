from uuid import UUID

from fastapi import FastAPI, Depends, status, Response, HTTPException
from typing import List

import uvicorn
from app import models as m

from app.database import engine, Session
from app import models, schemas

from app.hashing import Hash

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


@app.get(
    "/order/{id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.OrderResponseType,
    tags=["order"],
)
def view_order(id: UUID, response: Response, db: Session = Depends(db_connection)):
    order: m.Order = db.query(m.Order).filter_by(id=id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    return order


@app.get("/orders", response_model=List[schemas.OrderResponseType], tags=["order"])
def view_orders(db: Session = Depends(db_connection)):
    orders: List[m.Order] = db.query(m.Order).all()

    return orders


@app.post("/order", status_code=status.HTTP_201_CREATED, tags=["order"])
def create_order(
    request: schemas.OrderRequestType,
    response: Response,
    db: Session = Depends(db_connection),
):
    if db.query(m.Order).filter_by(code=request.code).first():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Order already existed"
        )
    else:
        new_order: m.Order = m.Order(customer=request.customer, code=request.code)
        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        return new_order


@app.delete("/order/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["order"])
def delete_order(id: UUID, db: Session = Depends(db_connection)):
    order = db.query(m.Order).filter(m.Order.id == id)
    if not order.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    else:
        order.delete(synchronize_session=False)
        db.commit()

    return "Deleted"


@app.put("/order/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["order"])
def update_order(
    id: UUID, request: schemas.OrderRequestType, db: Session = Depends(db_connection)
):
    order = db.query(m.Order).filter(m.Order.id == id)
    if not order.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    else:
        order.update(dict(code=request.code, customer=request.customer))
        db.commit()

    return "Updated"


@app.get("/user/{id}", response_model=schemas.UserResponseType, tags=["user"])
def view_user(id: UUID, db: Session = Depends(db_connection)):
    user = db.query(m.User).filter(m.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@app.post("/user", response_model=schemas.UserResponseType, tags=["user"])
def create_user(
    request: schemas.UserRequestType,
    db: Session = Depends(db_connection),
):
    new_user = m.User(
        name=request.name,
        email=request.email,
        password=Hash.bcrypt(password=request.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
