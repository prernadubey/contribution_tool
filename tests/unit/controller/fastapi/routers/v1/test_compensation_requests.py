import uuid
from unittest.mock import AsyncMock

from components.application.get_application_state import UseCaseResponse
from components.application.uc_response import UseCaseResponseStatus
from components.domain.activity_type import ActivityType
from components.domain.compensation_request import CompensationRequest
from components.domain.project import Project
from components.domain.skill import Skill
from components.domain.user import Trainer, User, UserRole

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
    role=UserRole.user,
    level="R1",
    employment_type="internal",
)

TS = 150000000

TEST_ACTIVITY_TYPE = ActivityType(id=1, name="test_activity_type")

TEST_UUID = uuid.uuid4()

EXAMPLE_COMPENSATION_REQUEST = [
    CompensationRequest(
        id=TEST_UUID,
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

SUCCESSFUL_RESPONSE = {
    "data": EXAMPLE_COMPENSATION_REQUEST,
    "status": UseCaseResponseStatus.SUCCESS,
    "error_detail": None,
    "code": None,
}

ENDPOINT_RESPONSE = [
    {
        "ID": str(TEST_UUID),
        "activityDate": "1974-10-03",
        "activityType": "test_activity_type",
        "courseID": "course1",
        "createdAtTs": 150000000,
        "createdBy": {
            "ID": 1,
            "email": "abcuser@gmail.com",
            "name": "UserName",
            "role": "user",
            "surname": "UserSurname",
        },
        "isRewarded": False,
        "project": {
            "ID": 1,
            "locations": ["Poland"],
            "name": "ProjectName",
            "type": "project_type_1",
        },
        "rdPoint": "2.5",
        "requestInitiator": {
            "ID": 1,
            "email": "abcuser@gmail.com",
            "name": "UserName",
            "role": "user",
            "surname": "UserSurname",
        },
        "status": "draft",
        "trainer": {
            "ID": "1",
            "email": "abcuser@gmail.com",
            "employment_type": "internal",
            "level": "R1",
            "name": "TrainerName",
            "role": "user",
            "surname": "TrainerSurname",
        },
        "trainingType": "other",
    }
]


def test_compensation_request__get_resource__data_returned(mocker, fastapi_test_client):
    uc_mock = mocker.patch(
        "components.controller.fastapi.routers.v1.compensation_requests.GetCompensationRequests"
    )
    uc_mock.return_value.execute = AsyncMock(
        return_value=UseCaseResponse(**SUCCESSFUL_RESPONSE)
    )
    response = fastapi_test_client.get("/v1/compensationRequests")

    assert response.status_code == 200
    assert response.json() == ENDPOINT_RESPONSE
