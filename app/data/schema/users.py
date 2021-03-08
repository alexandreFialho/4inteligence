from pydantic import BaseModel
from datetime import date


class UserBase(BaseModel):
    name: str
    document: str = "123.456.789-10"
    birth_date: date


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
