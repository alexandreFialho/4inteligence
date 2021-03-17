from typing import Optional
from pydantic import BaseModel, validator
from datetime import date

from data.schema.address import Address, AddressIn
from data.schema.helpers import validators


class UserBase(BaseModel):
    name: str
    document: str
    birth_date: date

    _empty_name = validator("name", allow_reuse=True)(validators.check_field_not_empty)
    _empty_document = validator("document", allow_reuse=True)(
        validators.check_field_not_empty
    )
    _normalize_name = validator("name")(validators.normalize)

    @validator("name")
    def name_must_contain_spaces(cls, name: str):
        name_split = name.split()
        if len(name_split) == 1:
            raise ValueError("must contain first and second name")
        return name

    @validator("document")
    def validate_document(cls, document: str):
        import re

        try:
            if not re.match(r"\d{3}\.\d{3}\.\d{3}-\d{2}", document):
                raise

            numbers = [int(digit) for digit in document if digit.isdigit()]

            if len(numbers) != 11 or len(set(numbers)) == 1:
                raise

            sum_of_products = sum(a * b for a, b in zip(numbers[0:9], range(10, 1, -1)))
            expected_digit = (sum_of_products * 10 % 11) % 10
            if numbers[9] != expected_digit:
                raise

            sum_of_products = sum(
                a * b for a, b in zip(numbers[0:10], range(11, 1, -1))
            )
            expected_digit = (sum_of_products * 10 % 11) % 10
            if numbers[10] != expected_digit:
                raise

        except:
            raise ValueError("Invalid document")

        return document


class UserIn(UserBase):
    address: Optional[AddressIn]


class UserPut(UserBase):
    name: Optional[str]
    document: Optional[str]
    birth_date: Optional[date]


class User(UserBase):
    id: int
    address: Optional[Address]

    class Config:
        orm_mode = True
