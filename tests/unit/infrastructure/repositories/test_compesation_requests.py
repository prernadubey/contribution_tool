from datetime import datetime
from unittest.mock import MagicMock, Mock

import pytest

from components.infrastructure.repositories.compensation_requests.compensation_requests_sql_repository import (
    CompensationRequestDTO,
    CompensationRequestsSQLRepository,
)

COMPENSATION_DB_TYPE_1 = {
    "id": 1,
    "status": "denied",
    "request_initiator_id": 1,
    "trainer_id": 1,
    "project_id": 1,
    "training_type": "internal_training",
    "created_by_id": 1,
    "created_at": datetime.fromisoformat("2023-06-01 20:11:22Z"),
    "activity_date": "2023-06-01",
    "activity_type_id": 2,
    "is_rewarded": True,
    "course_id": "AWS",
    "rd_point": 1.5,
    "skill_name": "Python",
}
COMPENSATION_DTO_TYPE_1 = {
    "id": 1,
    "status": "denied",
    "request_initiator_id": 1,
    "trainer_id": 1,
    "project_id": 1,
    "training_type": "internal_training",
    "created_by_id": 1,
    "created_at_ts": 1685650282,
    "activity_date": "2023-06-01",
    "activity_type_id": 2,
    "is_rewarded": True,
    "course_id": "AWS",
    "rd_point": 1.5,
    "skill": "Python",
}
COMPENSATION_DB_TYPE_2 = {
    "id": 2,
    "status": "pending",
    "request_initiator_id": 1,
    "trainer_id": 1,
    "project_id": 1,
    "training_type": "internal_training",
    "created_by_id": 1,
    "created_at": datetime.fromisoformat("2023-06-01 19:22:33Z"),
    "activity_date": "2023-05-01",
    "activity_type_id": 2,
    "is_rewarded": True,
    "course_id": "AWS",
    "rd_point": 1,
    "skill_name": "Python",
}
COMPENSATION_DTO_TYPE_2 = {
    "id": 2,
    "status": "pending",
    "request_initiator_id": 1,
    "trainer_id": 1,
    "project_id": 1,
    "training_type": "internal_training",
    "created_by_id": 1,
    "created_at_ts": 1685647353,
    "activity_date": "2023-05-01",
    "activity_type_id": 2,
    "is_rewarded": True,
    "course_id": "AWS",
    "rd_point": 1,
    "skill": "Python",
}


@pytest.fixture
def test_compensation_request_sql_repository(
    db_session_mock,
) -> CompensationRequestsSQLRepository:
    return CompensationRequestsSQLRepository(db_session=db_session_mock)


async def test_get_compensation_requests__requests_exists__returned_data(
    test_compensation_request_sql_repository,
):
    sql_ret1 = MagicMock()
    sql_ret1.configure_mock(**COMPENSATION_DB_TYPE_1)

    sql_ret2 = MagicMock()
    sql_ret2.configure_mock(**COMPENSATION_DB_TYPE_2)

    test_compensation_request_sql_repository.db_session.execute.return_value.fetchall = Mock(
        return_value=[sql_ret1, sql_ret2]
    )

    result = await test_compensation_request_sql_repository.get_compensation_requests()
    assert result == [
        CompensationRequestDTO(**COMPENSATION_DTO_TYPE_1),
        CompensationRequestDTO(**COMPENSATION_DTO_TYPE_2),
    ]


async def test_get_compensation__no_requests__returned_empty_list(
    test_compensation_request_sql_repository,
):
    test_compensation_request_sql_repository.db_session.execute.return_value.fetchall = Mock(
        return_value=[]
    )

    result = await test_compensation_request_sql_repository.get_compensation_requests()
    assert result == []
