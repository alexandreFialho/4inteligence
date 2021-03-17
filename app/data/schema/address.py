from typing import Optional
from pydantic import BaseModel, validator

from data.schema.helpers.validators import normalize


def validate_postalcode(cls, postal_code):
    import re

    if not re.match(r"\d{5}-\d{3}", postal_code):
        raise ValueError("Invalid postal code format")

    return postal_code


class AddressBase(BaseModel):
    street: Optional[str] = ""
    neighborhoods: Optional[str] = ""
    city: Optional[str] = ""
    state: Optional[str] = ""

    _street_normalize = validator("street", allow_reuse=True)(normalize)
    _neighborhoods_normalize = validator("neighborhoods", allow_reuse=True)(normalize)
    _city_normalize = validator("city", allow_reuse=True)(normalize)
    _state_normalize = validator("state", allow_reuse=True)(normalize)


class AddressPut(AddressBase):
    postal_code: Optional[str] = ""

    _postacode_validate = validator("postal_code", allow_reuse=True)(
        validate_postalcode
    )


class AddressIn(AddressBase):
    postal_code: str

    _postacode_validate = validator("postal_code", allow_reuse=True)(
        validate_postalcode
    )


class Address(AddressIn):
    id: int

    class Config:
        orm_mode = True
