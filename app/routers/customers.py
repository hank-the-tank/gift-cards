from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app import Session, schemas, Hash

from app import models as m

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("/{id}", response_model=schemas.CustomerResponseType)
def view_customers(id: UUID, db: Session = Depends(m.db_connection)):
    customer = db.query(m.Customer).filter(m.Customer.id == id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return customer


@router.post("/", response_model=schemas.CustomerResponseType)
def create_customers(
    request: schemas.CustomerRequestType,
    db: Session = Depends(m.db_connection),
):
    new_customer = m.Customer(
        name=request.name,
        email=request.email,
        password=Hash.bcrypt(password=request.password),
    )
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer
