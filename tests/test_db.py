import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from tests.config import DBConfig

engine = create_engine(DBConfig.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker()


@pytest.fixture(scope='module')
def connection():
    connection = engine.connect()
    yield connection
    connection.close()


@pytest.fixture(scope='function')
def session(connection):
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session
    session.close()
    transaction.rollback()