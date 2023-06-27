from unittest.mock import AsyncMock, MagicMock, Mock

import pytest

from components.domain.activity_type import ActivityType
from components.infrastructure.repositories.activity_types.activity_types_sql_repository import (
    ActivityTypesSQLRepository,
)

ACTIVITY_TYPE_1 = {"id": 1, "name": "Activity1"}
ACTIVITY_TYPE_2 = {"id": 2, "name": "Activity2"}


@pytest.fixture
def db_session_mock() -> ActivityTypesSQLRepository:
    return AsyncMock()


@pytest.fixture
def test_activity_types_sql_repository(db_session_mock) -> ActivityTypesSQLRepository:
    return ActivityTypesSQLRepository(db_session=db_session_mock)


#
#
# @pytest.fixture
# def get_application_status_uc(test_application_repository):
#     return GetApplicationStatus(application_repository=test_application_repository)


async def test_get_activity_types__activity_types_exists__returned_data(
    test_activity_types_sql_repository,
):
    sql_ret1 = MagicMock()
    sql_ret1.configure_mock(**ACTIVITY_TYPE_1)

    sql_ret2 = MagicMock()
    sql_ret2.configure_mock(**ACTIVITY_TYPE_2)

    test_activity_types_sql_repository.db_session.execute.return_value.fetchall = Mock(
        return_value=[sql_ret1, sql_ret2]
    )

    result = await test_activity_types_sql_repository.get_activity_types()
    assert result == [ActivityType(**ACTIVITY_TYPE_1), ActivityType(**ACTIVITY_TYPE_2)]


async def test_get_activity_types__no_activity_types__returned_empty_list(
    test_activity_types_sql_repository,
):
    test_activity_types_sql_repository.db_session.execute.return_value.fetchall = Mock(
        return_value=[]
    )

    result = await test_activity_types_sql_repository.get_activity_types()
    assert result == []
