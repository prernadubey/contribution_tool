import logging
import typing as t

from components.application.uc_base import UseCaseBase
from components.application.uc_request import GenericUseCaseRequest
from components.application.uc_response import (
    GenericUseCaseResponse,
    UseCaseErrorResponse,
    UseCaseResponseStatus,
)
from components.domain.application_status import ApplicationStatus
from components.infrastructure.repositories.application_status.interface import (
    ApplicationRepositoryProtocol,
)

_logger = logging.getLogger(__name__)

UseCaseRequest = GenericUseCaseRequest[None]
UseCaseResponse = GenericUseCaseResponse[ApplicationStatus]


class GetApplicationStatus(UseCaseBase):
    Request = UseCaseRequest
    Response = UseCaseResponse

    def __init__(self, application_repository: ApplicationRepositoryProtocol):
        self.application_repository = application_repository

    async def execute(
        self, request: UseCaseRequest
    ) -> t.Union[UseCaseResponse, UseCaseErrorResponse]:
        _logger.info(f"Processing use case with request.data:{request.data}")

        application_status: ApplicationStatus = (
            await self.application_repository.get_application_status()
        )

        return self.Response.build(
            status=UseCaseResponseStatus.SUCCESS, data=application_status
        )
