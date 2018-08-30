import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('DB_CONNECTION_URL')
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