from pydantic import BaseModel


class OrderRequestType(BaseModel):
    code: str
    customer: str


class OrderResponseType(BaseModel):
    code: str
    customer: str

    class Config:
        orm_mode = True


class UserRequestType(BaseModel):
    name: str
    email: str
    password: str


class UserResponseType(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True
