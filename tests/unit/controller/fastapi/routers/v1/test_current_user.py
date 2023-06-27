from unittest.mock import AsyncMock

from components.application.get_current_user import UseCaseResponse
from components.application.uc_response import UseCaseResponseStatus
from components.domain.user import User

API_RESPONSE = {
    "ID": 1000000000000000001,
    "name": "firstname",
    "surname": "surname",
    "email": "test@email.com",
    "role": "user",
}

TEST_USER_DATA = {
    "id": 1000000000000000001,
    "name": "firstname",
    "surname": "surname",
    "email": "test@email.com",
    "role": "user",
}

SUCCESSFUL_USER_RESPONSE = {
    "data": User(**TEST_USER_DATA),
    "status": UseCaseResponseStatus.SUCCESS,
    "error_detail": None,
    "code": None,
}

Failed_USER_RESPONSE = {
    "data": None,
    "status": UseCaseResponseStatus.SUCCESS,
    "error_detail": None,
    "code": None,
}


def test_current_user__get_resource__data_returned(mocker, fastapi_test_client):
    uc_mock = mocker.patch(
        "components.controller.fastapi.routers.v1.current_user.GetCurrentUser"
    )
    uc_mock.return_value.execute = AsyncMock(
        return_value=UseCaseResponse(**SUCCESSFUL_USER_RESPONSE)
    )
    response = fastapi_test_client.get(
        "/v1/users/me", headers={"X-User-ID": "1000000000000000001"}
    )

    assert response.status_code == 200
    assert response.json() == API_RESPONSE


def test_current_user__get_resource__data_not_returned(mocker, fastapi_test_client):
    uc_mock = mocker.patch(
        "components.controller.fastapi.routers.v1.current_user.GetCurrentUser"
    )
    uc_mock.return_value.execute = AsyncMock(
        return_value=UseCaseResponse(**Failed_USER_RESPONSE)
    )
    response = fastapi_test_client.get(
        "/v1/users/me", headers={"X-User-ID": "1000000000000000023"}
    )
    assert response.status_code == 500


def test_current_user__header_not_passed__unauthorized_returned(fastapi_test_client):
    response = fastapi_test_client.get("/v1/users/me")
    assert response.status_code == 401
