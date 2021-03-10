import requests
import re
import json

from sqlalchemy.exc import InvalidRequestError

from data.models import Address
from data.schema.address import AddressIn
from controllers.base_controller import CONTROLLER
from controllers.users import UserController


class AddressController(CONTROLLER):
    def __init__(self, db_session):
        super(AddressController, self).__init__(
            db_session=db_session, db_entity=Address
        )

    def create(self, address: AddressIn):
        address_dict = dict(address.dict())

        user = UserController(self.db_session).get(address.user_id)

        if not user:
            raise InvalidRequestError

        postal_code = "".join(re.findall(r"\d+", address.postal_code))

        if not len(postal_code) == 8:
            raise ValueError

        response = requests.get(f"https://viacep.com.br/ws/{postal_code}/json/")

        if not response.ok or json.loads(response.content).get("erro"):
            raise ValueError
        else:
            response = json.loads(response.content)

        via_cep_keys = {
            "street": "logradouro",
            "neighborhoods": "bairro",
            "city": "localidade",
            "state": "uf",
        }

        for key, value in address_dict.items():
            if key == "user_id" or value:
                continue

            address_dict[key] = response[via_cep_keys[key]]

        db_address = Address(**address_dict)
        self.db_session.add(db_address)
        self.db_session.commit()
        return self.get(db_address.id)
