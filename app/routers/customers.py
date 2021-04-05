from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app import Session, schemas, Hash, database as db, oauth2

from app import models as m

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get("/{id}", response_model=schemas.CustomerResponseType)
def view_customers(
    id: UUID,
    db: Session = Depends(db.db_connection),
    current_user: schemas.UserRequestType = Depends(oauth2.get_current_user),
):
    customer = db.query(m.Customer).filter(m.Customer.id == id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return customer


@router.post("/", response_model=schemas.CustomerResponseType)
def create_customers(
    request: schemas.CustomerRequestType,
    db: Session = Depends(db.db_connection),
    current_user: schemas.UserRequestType = Depends(oauth2.get_current_user),
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
