from sqlalchemy.orm.exc import UnmappedInstanceError

from core.controllers.base import BaseController
from core.controllers.users import UserController
from data.models import Address
from data.schema.address import AddressBase


class AddressController(BaseController):
    def __init__(self, db_session):
        super(AddressController, self).__init__(
            db_session=db_session, db_model=Address
        )

    def create(self, user_id: int, address: AddressBase):
        user = UserController(self.db_session).get(user_id)

        if not user:
            raise UnmappedInstanceError

        return super(AddressController, self).create(
            schema=address,
            user=user
        )
