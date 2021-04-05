from typing import List
from uuid import UUID

from fastapi import APIRouter, status, Response, Depends, HTTPException
from app import models as m
from app import database as db
from app import schemas, Session
from app import oauth2

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/", response_model=List[schemas.OrderResponseType])
def view_orders(
    db: Session = Depends(db.db_connection),
    current_user: schemas.UserRequestType = Depends(oauth2.get_current_user),
):
    orders: List[m.Order] = db.query(m.Order).all()

    return orders


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
def create_order(
    request: schemas.OrderRequestType,
    db: Session = Depends(db.db_connection),
    current_user: schemas.UserRequestType = Depends(oauth2.get_current_user),
):
    customer = db.query(m.Customer).first()
    if db.query(m.Order).filter_by(code=request.code).first():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Order already existed"
        )
    else:
        new_order: m.Order = m.Order(
            code=request.code,
            customer_id=customer.id,
        )
        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        return new_order


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.OrderResponseType,
)
def view_order(
    id: UUID,
    db: Session = Depends(db.db_connection),
    current_user: schemas.UserRequestType = Depends(oauth2.get_current_user),
):
    order: m.Order = db.query(m.Order).filter_by(id=id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    return order


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_order(
    id: UUID,
    db: Session = Depends(db.db_connection),
    current_user: schemas.UserRequestType = Depends(oauth2.get_current_user),
):
    order = db.query(m.Order).filter(m.Order.id == id)
    if not order.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    else:
        order.delete(synchronize_session=False)
        db.commit()

    return "Deleted"


@router.put(
    "/{id}",
    status_code=status.HTTP_202_ACCEPTED,
)
def update_order(
    id: UUID,
    request: schemas.OrderRequestType,
    db: Session = Depends(db.db_connection),
    current_user: schemas.UserRequestType = Depends(oauth2.get_current_user),
):
    order = db.query(m.Order).filter(m.Order.id == id)
    if not order.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    else:
        order.update(dict(code=request.code))
        db.commit()

    return "Updated"
