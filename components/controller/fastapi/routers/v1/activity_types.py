import typing as t

from fastapi import APIRouter, Depends

from components.application.get_activity_types import GetActivityTypes
from components.application.uc_response import UseCaseResponseStatus
from components.controller.fastapi.dependencies import get_activity_types_repository
from components.controller.fastapi.error_processor import (
    process_controller_error_usecase_response,
)
from components.controller.fastapi.response import ResponseBaseModel
from components.domain.activity_type import ActivityType

router = APIRouter(tags=["Activity Types"])


class ActivityTypeResponse(ResponseBaseModel):
    id: int
    name: str

    class Config(ResponseBaseModel.Config):
        schema_extra = {
            "example": {
                "id": 1,
                "name": "project education contribution",
            }
        }


@router.get("/activityTypes", response_model=t.List[ActivityTypeResponse])
async def get_activity(
    activity_repo=Depends(get_activity_types_repository),
):
    usecase = GetActivityTypes(activity_repo)

    uc_request = usecase.Request(data=None)
    uc_response = await usecase.execute(request=uc_request)

    if uc_response.status is not UseCaseResponseStatus.SUCCESS or not uc_response.data:
        return process_controller_error_usecase_response(use_case_response=uc_response)

    response_data: t.List[ActivityType] = uc_response.data
    return [
        ActivityTypeResponse(id=activity_type.id, name=activity_type.name)
        for activity_type in response_data
    ]
