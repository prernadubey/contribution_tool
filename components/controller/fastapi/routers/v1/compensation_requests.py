import typing as t
from dataclasses import asdict

from fastapi import APIRouter, Depends

from components.application.get_compensation_requests import GetCompensationRequests
from components.application.uc_response import UseCaseResponseStatus
from components.controller.fastapi.dependencies import (
    get_activity_types_repository,
    get_compensation_requests_repository,
    get_projects_repository,
    get_trainers_repository,
    get_users_repository,
)
from components.controller.fastapi.error_processor import (
    process_controller_error_usecase_response,
)
from components.controller.fastapi.routers.v1.schemas import (
    BaseRequestsResponse,
    CompensationRequestSchema,
)
from components.domain.compensation_request import CompensationRequest

router = APIRouter(tags=["Activity Types"])


class CompensationRequestsResponse(CompensationRequestSchema, BaseRequestsResponse):
    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "ID": "e2ef5ae2-f0ec-4f63-b940-2f160552cbc2",
                "status": "pending",
                "trainer": {
                    "ID": "4060000000000000000",
                    "name": "John Smith",
                    "email": "john_smith@epam.com",
                    "role": "user",
                    "level": "R1",
                    "employmentType": "internal",
                },
                "project": {
                    "ID": "1",
                    "name": "EPM-PRR",
                    "type": "some type",
                    "locations": ["loc_1", "loc_2"],
                },
                "trainingType": "internal_training",
                "requestInitiator": {
                    "ID": "4060000000000000002",
                    "name": "Peter Parker",
                    "email": "peter_parker@epam.com",
                    "role": "user",
                },
                "createdBy": {
                    "ID": "4060000000000000001",
                    "name": "Joe Doe",
                    "email": "joe_doe@epam.com",
                    "role": "user",
                },
                "createdAtTs": 1684790322,
                "activityType": "coordination",
                "activityDate": "2023-05-22",
                "courseID": 1234567,
                "skill": "Python",
                "rdPoint": 1.5,
                "isRewarded": True,
            }
        }


@router.get(
    "/compensationRequests", response_model=t.List[CompensationRequestsResponse]
)
async def get_compensation_requests(
    activity_types_repo=Depends(get_activity_types_repository),
    users_repo=Depends(get_users_repository),
    projects_repo=Depends(get_projects_repository),
    trainers_repo=Depends(get_trainers_repository),
    compensation_requests_repo=Depends(get_compensation_requests_repository),
):
    usecase = GetCompensationRequests(
        activity_types_sql_repository=activity_types_repo,
        projects_sql_repository=projects_repo,
        trainers_sql_repository=trainers_repo,
        users_sql_repository=users_repo,
        compensation_requests_sql_repository=compensation_requests_repo,
    )

    uc_request = usecase.Request(data=None)
    uc_response = await usecase.execute(request=uc_request)
    if uc_response.status is not UseCaseResponseStatus.SUCCESS or not uc_response.data:
        return process_controller_error_usecase_response(use_case_response=uc_response)

    response_data: t.List[CompensationRequest] = uc_response.data

    return [CompensationRequestsResponse(**asdict(r)) for r in response_data]
