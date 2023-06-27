import logging
import typing as t

from components.application.uc_base import UseCaseBase
from components.application.uc_request import GenericUseCaseRequest
from components.application.uc_response import (
    GenericUseCaseResponse,
    UseCaseErrorResponse,
    UseCaseResponseStatus,
)
from components.domain.repository_interfaces.users_interface import (
    UsersRepositoryProtocol,
)
from components.domain.user import User

_logger = logging.getLogger(__name__)

UseCaseRequest = GenericUseCaseRequest[t.Optional[dict]]
UseCaseResponse = GenericUseCaseResponse[t.Optional[User]]


class GetCurrentUser(UseCaseBase):
    Request = UseCaseRequest
    Response = UseCaseResponse

    def __init__(self, users_sql_repository: UsersRepositoryProtocol):
        self.users_sql_repository = users_sql_repository

    async def execute(
        self, request: UseCaseRequest
    ) -> t.Union[UseCaseResponse, UseCaseErrorResponse]:
        _logger.info(f"Processing use case with request.data:{request.data}")

        user_id: int = request.data.get("user_id")  # type: ignore
        user_data: t.Optional[User] = await self.users_sql_repository.get_user(user_id)

        return self.Response.build(status=UseCaseResponseStatus.SUCCESS, data=user_data)
