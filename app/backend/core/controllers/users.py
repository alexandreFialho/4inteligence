from core.controllers.base import BaseController
from data.models import User


class UserController(BaseController):
    def __init__(self, db_session):
        super(UserController, self).__init__(db_session=db_session, db_model=User)
