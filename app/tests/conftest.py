import os
import pytest
from typing import Generator
from contextlib import contextmanager

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database
from starlette.config import environ
from starlette.testclient import TestClient
from pydantic import PostgresDsn


from api.main import app
from data.database import DbSession, Base


SQLALCHEMY_DATABASE_URL = PostgresDsn.build(
    scheme="postgresql",
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_SERVER_TEST"),
    port=os.getenv("POSTGRES_PORT")
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_db_session() -> Generator:
    try:
        db = TestingSessionLocal()
        yield db
    except Exception as e:
        raise e


@pytest.fixture(scope="module", autouse=True)
def create_test_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[DbSession] = override_db_session


@pytest.fixture()
def client():
    with TestClient(app) as client:
        yield client