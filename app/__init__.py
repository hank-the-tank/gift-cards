from fastapi import FastAPI

import uvicorn

from app.database import engine, Session
from app import models, schemas
from app import authentication

from app.hashing import Hash

from app.routers import users, orders, customers

models.Base.metadata.create_all(engine)
app = FastAPI()


@app.get("/")
def index():
    return dict(data="landing page")


app.include_router(authentication.router)
app.include_router(users.router)
app.include_router(customers.router)
app.include_router(orders.router)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
