import typing as t

import pytest

from components.application.get_compensation_requests import GetCompensationRequests
from components.application.uc_response import UseCaseResponseStatus
from components.domain.activity_type import ActivityType
from components.domain.compensation_request import CompensationRequest
from components.domain.project import Project
from components.domain.repository_interfaces.activity_types_interface import (
    ActivityTypesRepositoryProtocol,
)
from components.domain.repository_interfaces.compensation_requests_interface import (
    CompensationRequestDTO,
    CompensationRequestsRepositoryProtocol,
)
from components.domain.repository_interfaces.projects_interface import (
    ProjectsRepositoryProtocol,
)
from components.domain.repository_interfaces.trainers_interface import (
    TrainersRepositoryProtocol,
)
from components.domain.repository_interfaces.users_interface import (
    UsersRepositoryProtocol,
)
from components.domain.skill import Skill
from components.domain.user import Trainer, User

TEST_USER = User(
    id=1, name="UserName", surname="UserSurname", email="abcuser@gmail.com", role="user"
)
TEST_PROJECT = Project(
    id=1, name="ProjectName", type="project_type_1", locations=["Poland"]
)
TEST_TRAINER = Trainer(
    id=1,
    name="TrainerName",
    surname="TrainerSurname",
    email="abcuser@gmail.com",
    role="trainer",
    level="R1",
    employment_type="internal",
)

TEST_ACTIVITY_TYPE = ActivityType(id=1, name="test_activity_type")


TS = 150000000

TEST_COMPENSATION_REQUEST = CompensationRequestDTO(
    id=1,
    status="draft",
    request_initiator_id=1,
    trainer_id=1,
    project_id=1,
    training_type="other",
    created_by_id=1,
    created_at_ts=TS,
    activity_date=TS,
    activity_type_id=1,
    is_rewarded=False,
    course_id="course1",
    rd_point=2.5,
    skill=Skill(id=1, name="python"),
)

EXAMPLE_COMPENSATION_REQUEST = [
    CompensationRequest(
        id=1,
        status="draft",
        created_by=TEST_USER,
        trainer=TEST_TRAINER,
        project=TEST_PROJECT,
        training_type="other",
        request_initiator=TEST_USER,
        created_at_ts=TS,
        activity_date=TS,
        activity_type="test_activity_type",
        is_rewarded=False,
        course_id="course1",
        rd_point=2.5,
        skill=Skill(id=1, name="python"),
    )
]

GET_USERS_RESPONSE = [TEST_USER]
GET_PROJECTS_RESPONSE = [TEST_PROJECT]
GET_TRAINERS_RESPONSE = [TEST_TRAINER]
GET_COMPENSATION_REQUESTS_RESPONSE = [TEST_COMPENSATION_REQUEST]
GET_ACTIVITY_TYPES_RESPONSE = [TEST_ACTIVITY_TYPE]


class TestUserRepository(UsersRepositoryProtocol):
    __test__ = False

    async def get_users(self, user_ids: t.List[int]) -> t.List[User]:
        return GET_USERS_RESPONSE

    # for the protocol interface
    async def get_user(self, user_id: int) -> User:
        pass


class TestProjectRepository(ProjectsRepositoryProtocol):
    __test__ = False

    async def get_projects(self, project_ids: t.List[int]) -> t.List[Project]:
        return GET_PROJECTS_RESPONSE


class TestTrainerRepository(TrainersRepositoryProtocol):
    __test__ = False

    async def get_trainers(self, trainer_ids: t.List[int]) -> t.List[Trainer]:
        return GET_TRAINERS_RESPONSE


class TestCompensationRequestsRepository(CompensationRequestsRepositoryProtocol):
    __test__ = False

    async def get_compensation_requests(
        self,
    ) -> t.List[CompensationRequest]:
        return GET_COMPENSATION_REQUESTS_RESPONSE


class TestActivityTypeRepository(ActivityTypesRepositoryProtocol):
    __test__ = False

    async def get_activity_types(
        self,
    ) -> t.List[ActivityType]:
        return GET_ACTIVITY_TYPES_RESPONSE


@pytest.fixture
def test_users_repository() -> TestUserRepository:
    return TestUserRepository()


@pytest.fixture
def test_projects_repository() -> TestProjectRepository:
    return TestProjectRepository()


@pytest.fixture
def test_trainers_repository() -> TestTrainerRepository:
    return TestTrainerRepository()


@pytest.fixture
def test_compensation_requests_repository() -> TestCompensationRequestsRepository:
    return TestCompensationRequestsRepository()


@pytest.fixture
def test_activity_types_repository() -> TestActivityTypeRepository:
    return TestActivityTypeRepository()


@pytest.fixture
def get_compensation_requests_uc(
    test_activity_types_repository,
    test_users_repository,
    test_projects_repository,
    test_trainers_repository,
    test_compensation_requests_repository,
):
    return GetCompensationRequests(
        activity_types_sql_repository=test_activity_types_repository,
        projects_sql_repository=test_projects_repository,
        users_sql_repository=test_users_repository,
        trainers_sql_repository=test_trainers_repository,
        compensation_requests_sql_repository=test_compensation_requests_repository,
    )


async def test_GetCompensationRequests__status_available__returned_status(
    get_compensation_requests_uc,
):
    uc_request = GetCompensationRequests.Request(data=None)
    uc_resp = await get_compensation_requests_uc.execute(uc_request)

    assert uc_resp.data == EXAMPLE_COMPENSATION_REQUEST
    assert uc_resp.status == UseCaseResponseStatus.SUCCESS
    assert uc_resp.error_detail is None
    assert uc_resp.code is None
