from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import Field

from components.application.get_application_state import GetApplicationStatus
from components.application.uc_response import UseCaseResponseStatus
from components.controller.fastapi.dependencies import get_application_repository
from components.controller.fastapi.error_processor import (
    process_controller_error_usecase_response,
)
from components.controller.fastapi.response import ResponseBaseModel
from components.domain.application_status import ApplicationStatus

router = APIRouter(tags=["Application status"])


class ApplicationStatusResponse(ResponseBaseModel):
    version: str
    app_name: Annotated[str, Field(alias="appName")]
    maintenance_mode: Annotated[bool, Field(alias="maintenanceMode")]

    class Config(ResponseBaseModel.Config):
        schema_extra = {
            "example": {
                "version": "v0.0.1",
                "appName": "abc",
                "maintenanceMode": False,
            }
        }


@router.get(
    "/applicationStatus",
    response_model=ApplicationStatusResponse,
    response_model_by_alias=True,
)
async def example(
    application_repo=Depends(get_application_repository),
):
    usecase = GetApplicationStatus(application_repo)
    uc_request = usecase.Request(data=None)
    uc_response = await usecase.execute(request=uc_request)

    if uc_response.status is not UseCaseResponseStatus.SUCCESS or not uc_response.data:
        return process_controller_error_usecase_response(use_case_response=uc_response)

    response_data: ApplicationStatus = uc_response.data

    return ApplicationStatusResponse(
        version=response_data.version,
        app_name=response_data.app_name,
        maintenance_mode=response_data.maintenance_mode,
    )
