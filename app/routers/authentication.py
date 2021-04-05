from datetime import timedelta

from fastapi import APIRouter, HTTPException, Depends, status

from app import models as m, Session, Hash
from app import database as db
from app import schemas
from app.routers import token

router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(request: schemas.LoginType, db: Session = Depends(db.db_connection)):
    user = db.query(m.User).filter(m.User.email == request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials"
        )
    if not Hash.verify(
        hashed_password=user.password, unhassed_password=request.password
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Password doesn't match the account",
        )

    access_token_expires = timedelta(minutes=token.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = token.create_access_token(
        data={"sub": user.email},
        # expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
