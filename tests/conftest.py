import datetime

import pytest
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from sqla_softdelete import SoftDeleteMixin
from .database import Base
from .database import DB_NAME


class Account(SoftDeleteMixin, Base):
    __tablename__ = 'accounts'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.Text, nullable=False)
    email = sa.Column(sa.String(128), nullable=False, index=True)

    logins = sa.orm.relationship('Login')

    def __init__(self, name: str = '', email: str = '', phone: str = ''):
        self.name = name
        self.email = email
        self.phone = phone

    def __repr__(self):
        return f'Account(id={self.id}, name={self.name}, email={self.email})'

    def __str__(self):
        return f'{self.name}: {self.email})'


class Login(SoftDeleteMixin, Base):
    __tablename__ = 'logins'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    account_id = sa.Column(sa.Integer, sa.ForeignKey('accounts.id'), nullable=False)
    logged_at = sa.Column(sa.DateTime(timezone=True), nullable=False, default=datetime.datetime.now())

    def __repr__(self):
        return f'Login(id={self.id}, account_id={self.account_id}, logged_at={self.logged_at})'


@pytest.fixture(scope='session')
def engine():
    return create_engine(DB_NAME)


@pytest.fixture(scope='session')
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def dbsession(engine, tables) -> Session:
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()
