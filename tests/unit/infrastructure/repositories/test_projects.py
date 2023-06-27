from unittest.mock import MagicMock, Mock

import pytest

from components.domain.project import Project
from components.infrastructure.repositories.projects.projects_sql_repository import (
    ProjectsSQLRepository,
)


@pytest.fixture
def test_projects_sql_repository(db_session_mock) -> ProjectsSQLRepository:
    return ProjectsSQLRepository(db_session=db_session_mock)


EXAMPLE_PROJECT_1_1 = {
    "id": 1,
    "name": "project_name_1",
    "type": "project_type_1",
    "location": "Poland",
}
EXAMPLE_PROJECT_1_2 = {
    "id": 1,
    "name": "project_name_1",
    "type": "project_type_1",
    "location": "Cuba",
}
EXAMPLE_PROJECT_2 = {
    "id": 2,
    "name": "project_name_2",
    "type": "project_type_2",
    "location": "Poland",
}


async def test_get_projects__project_exist__returned_data(test_projects_sql_repository):
    # 1 object
    sql_ret1 = MagicMock()
    sql_ret1.configure_mock(**EXAMPLE_PROJECT_1_1)
    sql_ret2 = MagicMock()
    sql_ret2.configure_mock(**EXAMPLE_PROJECT_1_2)
    sql_ret3 = MagicMock()
    sql_ret3.configure_mock(**EXAMPLE_PROJECT_2)
    test_projects_sql_repository.db_session.execute.return_value.fetchall = Mock(
        return_value=[sql_ret1, sql_ret2, sql_ret3]
    )
    result = await test_projects_sql_repository.get_projects()
    assert result == [
        Project(1, "project_name_1", "project_type_1", ["Poland", "Cuba"]),
        Project(2, "project_name_2", "project_type_2", ["Poland"]),
    ]


async def test_get_projects__filter_project_ids_and_projects_exist__returned_data(
    test_projects_sql_repository,
):
    # 1 object
    sql_ret1 = MagicMock()
    sql_ret1.configure_mock(**EXAMPLE_PROJECT_1_1)
    sql_ret2 = MagicMock()
    sql_ret2.configure_mock(**EXAMPLE_PROJECT_1_2)

    test_projects_sql_repository.db_session.execute.return_value.fetchall = Mock(
        return_value=[sql_ret1, sql_ret2]
    )
    result = await test_projects_sql_repository.get_projects(
        project_ids=[
            1,
        ]
    )

    assert "WHERE projects.id IN" in str(
        test_projects_sql_repository.db_session.execute.call_args.args[0]
    )

    assert result == [
        Project(1, "project_name_1", "project_type_1", ["Poland", "Cuba"])
    ]


async def test_get_projects__no_projects__returned_empty_list(
    test_projects_sql_repository,
):
    # no objects
    test_projects_sql_repository.db_session.execute.return_value.fetchall = Mock(
        return_value=[]
    )
    result = await test_projects_sql_repository.get_projects()
    assert result == []
