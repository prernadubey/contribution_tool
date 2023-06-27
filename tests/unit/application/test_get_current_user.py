import typing as t

import pytest

from components.application.get_current_user import GetCurrentUser
from components.application.uc_response import UseCaseResponseStatus
from components.domain.repository_interfaces.users_interface import (
    UsersRepositoryProtocol,
)
from components.domain.user import User

EXAMPLE_USER = User(
    id=1000000000000000001,
    name="test_user",
    surname="test_surname",
    email="test@email.com",
    role="user",
)


class TestUserSQLRepository(UsersRepositoryProtocol):
    __test__ = False

    async def get_user(self, user_id: int) -> t.Optional[User]:
        return EXAMPLE_USER

    async def get_users(self):
        pass


@pytest.fixture
def test_users_sql_repository() -> TestUserSQLRepository:
    return TestUserSQLRepository()


@pytest.fixture
def test_get_current_user_usercase(test_users_sql_repository):
    return GetCurrentUser(users_sql_repository=test_users_sql_repository)


async def test_get_current_user__user_exist__return_data(
    test_get_current_user_usercase,
):
    uc_request = GetCurrentUser.Request(data={"user_id": 1000000000000000001})
    uc_resp = await test_get_current_user_usercase.execute(uc_request)

    assert uc_resp.data == EXAMPLE_USER
    assert uc_resp.status == UseCaseResponseStatus.SUCCESS
    assert uc_resp.error_detail is None
    assert uc_resp.code is None
