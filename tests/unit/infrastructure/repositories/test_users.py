from unittest.mock import MagicMock, Mock

import pytest

from components.domain.user import User
from components.infrastructure.repositories.users.users_sql_repository import (
    UsersSQLRepository,
)


@pytest.fixture
def test_users_sql_repository(db_session_mock) -> UsersSQLRepository:
    return UsersSQLRepository(db_session=db_session_mock)


EXAMPLE_USER_1 = {
    "id": 42,
    "name": "hello",
    "surname": "hello",
    "email": "abc@bonjour.com",
    "role": "user",
}
EXAMPLE_USER_2 = {
    "id": 5,
    "name": "abba",
    "surname": "hello",
    "email": "fdas@hej.com",
    "role": "user",
}
EXAMPLE_USER_3 = {
    "id": 123,
    "name": "hi",
    "surname": "hello",
    "email": "abd@hello.com",
    "role": "user",
}


async def test_get_users__users_exist__returned_data(test_users_sql_repository):
    sql_ret1 = MagicMock()
    sql_ret1.configure_mock(**EXAMPLE_USER_1)

    sql_ret2 = MagicMock()
    sql_ret2.configure_mock(**EXAMPLE_USER_2)

    sql_ret3 = MagicMock()
    sql_ret3.configure_mock(**EXAMPLE_USER_3)

    test_users_sql_repository.db_session.execute.return_value.fetchall = Mock(
        return_value=[sql_ret1, sql_ret2, sql_ret3]
    )
    result = await test_users_sql_repository.get_users()
    assert result == [
        User(**EXAMPLE_USER_1),
        User(**EXAMPLE_USER_2),
        User(**EXAMPLE_USER_3),
    ]


async def test_get_users__filter_user_ids_and_users_exist__returned_data(
    test_users_sql_repository,
):
    sql_ret1 = MagicMock()
    sql_ret1.configure_mock(**EXAMPLE_USER_1)

    test_users_sql_repository.db_session.execute.return_value.fetchall = Mock(
        return_value=[sql_ret1]
    )
    result = await test_users_sql_repository.get_users(user_ids=[EXAMPLE_USER_1["id"]])

    assert "WHERE users.id IN" in str(
        test_users_sql_repository.db_session.execute.call_args.args[0]
    )

    assert result == [User(**EXAMPLE_USER_1)]


async def test_get_users__no_users__returned_empty_list(test_users_sql_repository):
    # no objects
    test_users_sql_repository.db_session.execute.return_value.fetchall = Mock(
        return_value=[]
    )
    result = await test_users_sql_repository.get_users()
    assert result == []


async def test_get_user__user_exist__returned_data(
    test_users_sql_repository,
):
    sql_ret1 = MagicMock()
    sql_ret1.configure_mock(**EXAMPLE_USER_1)

    test_users_sql_repository.db_session.execute.return_value.one_or_none = Mock(
        return_value=sql_ret1
    )
    result = await test_users_sql_repository.get_user(user_id=EXAMPLE_USER_1["id"])

    assert result == User(**EXAMPLE_USER_1)


async def test_get_user__user_not_exist__returned_none(test_users_sql_repository):
    # no objects
    test_users_sql_repository.db_session.execute.return_value.one_or_none = Mock(
        return_value=None
    )
    result = await test_users_sql_repository.get_user(user_id=EXAMPLE_USER_3["id"])
    assert not result
