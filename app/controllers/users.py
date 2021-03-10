from data.models import User
from controllers.base_controller import CONTROLLER


class UserController(CONTROLLER):
    def __init__(self, db_session):
        super(UserController, self).__init__(db_session=db_session, db_entity=User)
