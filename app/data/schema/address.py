from typing import Optional
from pydantic import BaseModel


class AddressBase(BaseModel):
    postal_code: str = "12345-678"


class AddressIn(AddressBase):
    street: Optional[str] = None
    neighborhoods: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None


class AddressUser(AddressBase):
    street: str
    neighborhoods: str
    city: str
    state: str


class Address(AddressUser):
    id: int
    user_id: int

    class Config:
        orm_mode = True
