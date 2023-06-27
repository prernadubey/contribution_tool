from unittest.mock import AsyncMock

from components.application.get_application_state import UseCaseResponse
from components.application.uc_response import UseCaseResponseStatus
from components.controller.fastapi.routers.v1.application_status import (
    ApplicationStatusResponse,
)

EXAMPLE_APPLICATION_STATUS_CAMEL = {
    "version": "1.1.1",
    "appName": "test_app_name",
    "maintenanceMode": 1,
}

EXAMPLE_APPLICATION_STATUS = {
    "version": "1.1.1",
    "app_name": "test_app_name",
    "maintenance_mode": 1,
}

SUCCESSFUL_RESPONSE = {
    "data": ApplicationStatusResponse(**EXAMPLE_APPLICATION_STATUS),
    "status": UseCaseResponseStatus.SUCCESS,
    "error_detail": None,
    "code": None,
}


def test_application_status__get_resource__data_returned(mocker, fastapi_test_client):
    uc_mock = mocker.patch(
        "components.controller.fastapi.routers.v1.application_status.GetApplicationStatus"
    )
    uc_mock.return_value.execute = AsyncMock(
        return_value=UseCaseResponse(**SUCCESSFUL_RESPONSE)
    )
    response = fastapi_test_client.get("/v1/applicationStatus")

    assert response.status_code == 200
    assert response.json() == EXAMPLE_APPLICATION_STATUS_CAMEL
