from typing import Optional
from pydantic import BaseModel


class AddressBase(BaseModel):
    postal_code: str


class AddressIn(AddressBase):
    street: Optional[str] = ""
    neighborhoods: Optional[str] = ""
    city: Optional[str] = ""
    state: Optional[str] = ""


class Address(AddressIn):
    id: int

    class Config:
        orm_mode = True
