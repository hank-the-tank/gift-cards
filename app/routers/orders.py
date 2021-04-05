from typing import List
from uuid import UUID

from fastapi import APIRouter, status, Response, Depends, HTTPException
from app import models as m

from app import schemas, Session

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/", response_model=List[schemas.OrderResponseType])
def view_orders(db: Session = Depends(m.db_connection)):
    orders: List[m.Order] = db.query(m.Order).all()

    return orders


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
def create_order(
    request: schemas.OrderRequestType,
    response: Response,
    db: Session = Depends(m.db_connection),
):
    if db.query(m.Order).filter_by(code=request.code).first():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Order already existed"
        )
    else:
        new_order: m.Order = m.Order(
            code=request.code,
            customer_id="b0e484d5-0bd9-4c81-8722-209cc5ff7301",
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
def view_order(id: UUID, response: Response, db: Session = Depends(m.db_connection)):
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
def delete_order(id: UUID, db: Session = Depends(m.db_connection)):
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
    id: UUID, request: schemas.OrderRequestType, db: Session = Depends(m.db_connection)
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
