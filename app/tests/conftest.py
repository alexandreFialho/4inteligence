import pytest
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from starlette.testclient import TestClient
from pydantic import PostgresDsn

from api import config
from api.main import app
from api.deps import DbSession
from data.database import Base


SQLALCHEMY_DATABASE_URL = PostgresDsn.build(
    scheme="postgresql",
    user=config.POSTGRES_USER,
    password=config.POSTGRES_PASSWORD,
    host=config.POSTGRES_SERVER_TEST,
    port=config.POSTGRES_PORT,
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False,
                                   bind=engine)


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
