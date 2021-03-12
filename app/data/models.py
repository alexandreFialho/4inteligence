from sqlalchemy import Column, ForeignKey, Integer, String, Date, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

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
