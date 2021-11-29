import pytest
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.exc import ObjectDeletedError

from tests.conftest import Account, Login


@pytest.mark.db
def test_query_all(dbsession):
    # Arrange
    account1 = Account(name='account1')
    account2 = Account(name='account2')

    dbsession.add_all([account1, account2])
    dbsession.flush()

    # Act

    actual_accounts = dbsession.execute(select(Account)).scalars().all()

    # Assert
    assert set(actual_accounts) == {account1, account2}


@pytest.mark.db
def test_get_all_not_deleted(dbsession):
    # Arrange
    account1 = Account(name='account1')
    account2 = Account(name='account2')
    account1.delete()

    dbsession.add_all([account1, account2])
    dbsession.flush()

    # Act
    actual_accounts = dbsession.execute(select(Account)).scalars().all()

    # Assert
    assert actual_accounts == [account2]


@pytest.mark.db
def test_filter_not_deleted(dbsession):
    # Arrange
    account1 = Account(name='account1')
    account2 = Account(name='account2')
    account3 = Account(name='account2')
    account1.delete()

    dbsession.add_all([account1, account2, account3])
    dbsession.flush()

    # Act
    actual_accounts = dbsession.execute(select(Account).where(Account.name == 'account2')).scalars().all()

    # Assert
    assert actual_accounts == [account2, account3]


@pytest.mark.db
def test_get_not_deleted(dbsession):
    # Arrange
    account = Account(name='account')

    dbsession.add(account)
    dbsession.flush()

    # Act
    actual_account = dbsession.get(Account, account.id)

    # Assert
    assert actual_account == account


@pytest.mark.db
def test_get_deleted(dbsession):
    # Arrange
    account = Account(name='account')
    account.delete()

    dbsession.add(account)
    dbsession.flush()
    dbsession.expire(account)

    # Act & Assert
    with pytest.raises(ObjectDeletedError):
        dbsession.get(Account, account.id)


@pytest.mark.db
def test_get_deleted_entity(dbsession):
    # Arrange
    account = Account(name='account')
    account.delete()

    dbsession.add(account)
    dbsession.flush()
    dbsession.expire(account)

    # Act & Assert
    with pytest.raises(ObjectDeletedError):
        dbsession.execute(select(Account).where(Account.id == account.id)).scalar()


@pytest.mark.db
def test_get_relation(dbsession):
    # Arrange
    account = Account(name='account')
    account.logins = [Login(), Login(), Login()]

    dbsession.add(account)
    dbsession.flush()
    dbsession.expire(account)

    # Act & Assert
    assert len(account.logins) == 3


@pytest.mark.db
def test_get_relation_lazy_deleted(dbsession):
    # Arrange
    account = Account(name='account')
    account.logins = [Login(), Login(), Login()]
    account.logins[0].delete()

    dbsession.add(account)
    dbsession.flush()
    dbsession.expire(account)

    # Act & Assert
    assert len(account.logins) == 2


@pytest.mark.db
def test_get_relation_joined_deleted(dbsession):
    # Arrange
    account = Account(name='account')
    account.logins = [Login(), Login(), Login()]
    account.logins[0].delete()

    dbsession.add(account)
    dbsession.flush()
    dbsession.expire(account)

    # Act & Assert
    fetched: Account = dbsession.get(Account, account.id, options=[joinedload(Account.logins)])
    assert len(fetched.logins) == 2
