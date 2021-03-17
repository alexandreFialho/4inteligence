from sqlalchemy import Column, ForeignKey, Integer, String, Date, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from pycep_correios import get_address_from_cep, WebService, exceptions

from data.database import Base


class AuthUser(Base):
    __tablename__ = "authuser"

    id = Column("id", Integer, primary_key=True, index=True)
    username = Column("username", String(30), unique=True, nullable=False)
    password = Column("hashed_password", String, nullable=False)
    full_name = Column("full_name", String(30), nullable=True)
    email = Column("email", String, unique=True, nullable=True)
    disabled = Column("disable", Boolean, nullable=True)
    create_at = Column("create_at", DateTime, default=func.now(), nullable=False)


class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, index=True)
    name = Column("name", String(30), nullable=False)
    document = Column("document", String(30), unique=True, nullable=False)
    birth_date = Column("birth_date", Date, nullable=False)
    created_date = Column("created_date", DateTime, default=func.now(), nullable=False)
    address = relationship(
        "Address",
        uselist=False,
        back_populates="user",
        cascade="all, delete",
        passive_deletes=True,
    )

    def __init__(self, **kwargs):
        if kwargs.get("address"):
            self.address = Address(**kwargs.pop("address"))

        super(User, self).__init__(**kwargs)


class Address(Base):
    __tablename__ = "address"

    id = Column("id", Integer, primary_key=True, index=True)
    user_id = Column(
        "user_id",
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    user = relationship("User", back_populates="address")
    postal_code = Column("postal_code", String, nullable=False)
    street = Column("street", String)
    neighborhoods = Column("neighborhoods", String)
    city = Column("city", String)
    state = Column("state", String)

    def __init__(self, **kwargs):
        address_viacep = self.get_address_with_postal_code(kwargs.get("postal_code"))

        for key, value in kwargs.items():
            if not value:
                kwargs[key] = address_viacep[key]

        super(Address, self).__init__(**kwargs)

    @classmethod
    def get_address_with_postal_code(self, postal_code: str):
        try:
            address_viacep = get_address_from_cep(
                postal_code, webservice=WebService.APICEP
            )

            return {
                "street": address_viacep.get("logradouro"),
                "neighborhoods": address_viacep.get("bairro"),
                "city": address_viacep.get("cidade"),
                "state": address_viacep.get("uf"),
            }

        except (exceptions.InvalidCEP, exceptions.CEPNotFound):
            raise ValueError
        except (
            ConnectionError,
            exceptions.Timeout,
            exceptions.HTTPError,
            exceptions.BaseException,
        ):
            "I accepted pass here because integration exceptions with api, dont must impeditive"
            pass
