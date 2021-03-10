from sqlalchemy import Column, ForeignKey, Integer, String, Date, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from data.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, index=True)
    name = Column("name", String(30), nullable=False)
    document = Column("document", String(30), unique=True, nullable=False)
    birth_date = Column("date", Date, nullable=False)
    created_date = Column("created_date", DateTime, default=func.now(), nullable=False)
    address = relationship("Address", uselist=False, back_populates="user")


class Address(Base):
    __tablename__ = "address"

    id = Column("id", Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="address")
    postal_code = Column("postal_code", String, nullable=False)
    street = Column("street", String)
    neighborhoods = Column("neighborhoods", String)
    city = Column("city", String)
    state = Column("state", String)
