import pytest
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database
from starlette.testclient import TestClient
from pydantic import PostgresDsn

from api.main import app
from core.config import settings
from data.database import Base, DbSession


SQLALCHEMY_DATABASE_URL = PostgresDsn.build(
    scheme="postgresql",
    user=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD,
    host=settings.POSTGRES_SERVER,
    path=f"/{settings.POSTGRES_DB}_test",
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
    finally:
        db.close()


@pytest.fixture(scope="module", autouse=True)
def create_test_database():
    if database_exists(SQLALCHEMY_DATABASE_URL):
        drop_database(SQLALCHEMY_DATABASE_URL)
    create_database(SQLALCHEMY_DATABASE_URL)
    Base.metadata.create_all(engine)
    app.dependency_overrides[DbSession] = override_db_session
    yield
    drop_database(SQLALCHEMY_DATABASE_URL)


@pytest.fixture()
def client():
    with TestClient(app) as client:
        yield client
