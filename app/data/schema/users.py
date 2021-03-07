from pydantic import BaseModel
from datetime import date, datetime


class UserBase(BaseModel):
    name: str
    document: str = "123.456.789-10"
    birth_date: date


class User(UserBase):
    id: int
    created_date: datetime

    class Config:
        orm_mode = True
