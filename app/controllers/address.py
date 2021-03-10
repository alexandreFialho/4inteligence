import requests
import re
import json

from data.models import Address
from data.schema.address import AddressIn
from controllers.base_controller import CONTROLLER


class AddressController(CONTROLLER):
    def __init__(self, db_session):
        super(AddressController, self).__init__(
            db_session=db_session, db_entity=Address
        )

    def create(self, address: AddressIn):
        address_dict = dict(address.dict())

        via_cep_keys = {
            "street": "logradouro",
            "neighborhoods": "bairro",
            "city": "localidade",
            "state": "uf",
        }

        postal_code = "".join(re.findall("\d+", address.postal_code))

        if not len(postal_code) == 8:
            raise ValueError

        response = json.loads(
            requests.get(f"https://viacep.com.br/ws/{postal_code}/json/").content
        )
        for key, value in address_dict.items():
            if value:
                continue

            address_dict[key] = response[via_cep_keys[key]]

        db_address = Address(**address_dict)
        self.db_session.add(db_address)
        self.db_session.commit()
        return self.get(db_address.id)
