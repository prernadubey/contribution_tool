import pytest

from components.application.get_application_state import GetApplicationStatus
from components.application.uc_response import UseCaseResponseStatus
from components.domain.application_status import ApplicationStatus
from components.infrastructure.repositories.application_status.interface import (
    ApplicationRepositoryProtocol,
)

EXAMPLE_APPLICATION_STATUS = ApplicationStatus(
    version="1.1.1", app_name="test_app_name", maintenance_mode=False
)


class TestApplicationRepository(ApplicationRepositoryProtocol):
    __test__ = False

    async def get_application_status(self) -> ApplicationStatus:
        return EXAMPLE_APPLICATION_STATUS

    async def turn_on_maintenance_mode(self) -> None:
        ...

    async def turn_off_maintenance_mode(self) -> None:
        ...


@pytest.fixture
def test_application_repository() -> TestApplicationRepository:
    return TestApplicationRepository()


@pytest.fixture
def get_application_status_uc(test_application_repository):
    return GetApplicationStatus(application_repository=test_application_repository)


async def test_GetApplicationStatus__status_available__returned_status(
    get_application_status_uc,
):
    uc_request = GetApplicationStatus.Request(data=None)
    uc_resp = await get_application_status_uc.execute(uc_request)

    assert uc_resp.data == EXAMPLE_APPLICATION_STATUS
    assert uc_resp.status == UseCaseResponseStatus.SUCCESS
    assert uc_resp.error_detail is None
    assert uc_resp.code is None
