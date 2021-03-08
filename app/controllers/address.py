from sqlalchemy.orm import Session

from data.models import Address

from .base_controller import CRUD


class Address_Controller(CRUD):

    def __init__(self, db: Session):
        super(Address_Controller, self).__init__(db, Address)
