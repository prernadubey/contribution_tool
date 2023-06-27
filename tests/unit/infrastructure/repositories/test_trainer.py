from unittest.mock import AsyncMock, MagicMock, Mock

import pytest

from components.domain.user import Trainer
from components.infrastructure.repositories.trainer.trainer_sql_repository import (
    TrainersSQLRepository,
)

TRAINER_EXAMPLE_1 = {
    "id": 1000000000000000011,
    "name": "John",
    "surname": "Smith",
    "email": "test@email.com",
    "role": "user",
    "trainer_level": "R1",
    "employment_type": "internal",
}
TRAINER_EXAMPLE_2 = {
    "id": 1000000000000000012,
    "name": "Alex",
    "surname": "Smith",
    "email": "test2@email.com",
    "role": "user",
    "trainer_level": "R2",
    "employment_type": "external",
}


@pytest.fixture
def db_session_mock() -> TrainersSQLRepository:
    return AsyncMock()


@pytest.fixture
def test_trainer_sql_repository(db_session_mock) -> TrainersSQLRepository:
    return TrainersSQLRepository(db_session=db_session_mock)


async def test_get_trainers__trainers_exists__returned_data(
    test_trainer_sql_repository,
):
    sql_ret1 = MagicMock()
    sql_ret1.configure_mock(**TRAINER_EXAMPLE_1)

    sql_ret2 = MagicMock()
    sql_ret2.configure_mock(**TRAINER_EXAMPLE_2)

    test_trainer_sql_repository.db_session.execute.return_value.fetchall = Mock(
        return_value=[sql_ret1, sql_ret2]
    )

    result = await test_trainer_sql_repository.get_trainers()
    assert result == [
        Trainer(
            id=TRAINER_EXAMPLE_1.get("id"),
            name=TRAINER_EXAMPLE_1.get("name"),
            surname=TRAINER_EXAMPLE_1.get("surname"),
            email=TRAINER_EXAMPLE_1.get("email"),
            role=TRAINER_EXAMPLE_1.get("role"),
            level=TRAINER_EXAMPLE_1.get("trainer_level"),
            employment_type=TRAINER_EXAMPLE_1.get("employment_type"),
        ),
        Trainer(
            id=TRAINER_EXAMPLE_2.get("id"),
            name=TRAINER_EXAMPLE_2.get("name"),
            surname=TRAINER_EXAMPLE_2.get("surname"),
            email=TRAINER_EXAMPLE_2.get("email"),
            role=TRAINER_EXAMPLE_2.get("role"),
            level=TRAINER_EXAMPLE_2.get("trainer_level"),
            employment_type=TRAINER_EXAMPLE_2.get("employment_type"),
        ),
    ]


async def test_get_trainers__filter_trainer_ids_and_trainers_exist__returned_data(
    test_trainer_sql_repository,
):
    sql_ret1 = MagicMock()
    sql_ret1.configure_mock(**TRAINER_EXAMPLE_1)

    test_trainer_sql_repository.db_session.execute.return_value.fetchall = Mock(
        return_value=[sql_ret1]
    )

    result = await test_trainer_sql_repository.get_trainers(
        trainer_ids=[
            1000000000000000011,
        ]
    )

    assert "WHERE users.id IN" in str(
        test_trainer_sql_repository.db_session.execute.call_args.args[0]
    )

    assert result == [
        Trainer(
            id=TRAINER_EXAMPLE_1.get("id"),
            name=TRAINER_EXAMPLE_1.get("name"),
            surname=TRAINER_EXAMPLE_1.get("surname"),
            email=TRAINER_EXAMPLE_1.get("email"),
            role=TRAINER_EXAMPLE_1.get("role"),
            level=TRAINER_EXAMPLE_1.get("trainer_level"),
            employment_type=TRAINER_EXAMPLE_1.get("employment_type"),
        )
    ]


async def test_get_trainer__no_trainers__returned_empty_list(
    test_trainer_sql_repository,
):
    test_trainer_sql_repository.db_session.execute.return_value.fetchall = Mock(
        return_value=[]
    )

    result = await test_trainer_sql_repository.get_trainers()
    assert result == []
