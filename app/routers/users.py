from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app import Session, schemas, Hash, oauth2

from app import models as m
from app import database as db

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{id}", response_model=schemas.UserResponseType)
def view_user(
    id: UUID,
    db: Session = Depends(db.db_connection),
    current_user: schemas.UserRequestType = Depends(oauth2.get_current_user),
):
    user = db.query(m.User).filter(m.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.post("/", response_model=schemas.UserResponseType)
def create_user(
    request: schemas.UserRequestType,
    db: Session = Depends(db.db_connection),
    current_user: schemas.UserRequestType = Depends(oauth2.get_current_user),
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
