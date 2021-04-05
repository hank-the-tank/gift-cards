from datetime import timedelta

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from app import models as m

from app.database import Session
from app.hashing import Hash
from app import jwt_token

from app import database as db
from app import schemas


router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(
    request: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(db.db_connection),
):
    user = db.query(m.User).filter(m.User.email == request.username).first()
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

    access_token_expires = timedelta(minutes=jwt_token.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt_token.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
