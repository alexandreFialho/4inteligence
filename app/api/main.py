from fastapi import FastAPI

from api.routers import users, address
from data.models import Base
from data.database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users.router)
app.include_router(address.router)
