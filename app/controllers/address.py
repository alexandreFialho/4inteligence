from sqlalchemy.orm.exc import UnmappedInstanceError

from data.models import Address
from data.schema.address import AddressBase
from controllers.base_controller import CONTROLLER
from controllers.users import UserController


class AddressController(CONTROLLER):
    def __init__(self, db_session):
        super(AddressController, self).__init__(
            db_session=db_session, db_model=Address
        )

    def create(self, user_id: int, address: AddressBase):
        user = UserController(self.db_session).get(user_id)

        if not user:
            raise UnmappedInstanceError

        db_address = Address(user=user, **address.dict())
        self.db_session.add(db_address)
        self.db_session.commit()
        return self.get(db_address.id)
