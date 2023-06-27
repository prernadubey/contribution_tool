import logging
import typing as t

from components.application.uc_base import UseCaseBase
from components.application.uc_request import GenericUseCaseRequest
from components.application.uc_response import (
    GenericUseCaseResponse,
    UseCaseErrorResponse,
    UseCaseResponseStatus,
)
from components.domain.activity_type import ActivityType
from components.domain.repository_interfaces.activity_types_interface import (
    ActivityTypesRepositoryProtocol,
)

_logger = logging.getLogger(__name__)

UseCaseRequest = GenericUseCaseRequest[None]
UseCaseResponse = GenericUseCaseResponse[t.List[ActivityType]]


class GetActivityTypes(UseCaseBase):
    Request = UseCaseRequest
    Response = UseCaseResponse

    def __init__(self, activity_types_repository: ActivityTypesRepositoryProtocol):
        self.activity_types_repository = activity_types_repository

    async def execute(
        self, request: UseCaseRequest
    ) -> t.Union[UseCaseResponse, UseCaseErrorResponse]:
        _logger.info(f"Processing use case with request.data:{request.data}")

        activity_types: t.List[
            ActivityType
        ] = await self.activity_types_repository.get_activity_types()

        return self.Response.build(
            status=UseCaseResponseStatus.SUCCESS, data=activity_types
        )
