import typing as t
from abc import abstractmethod

from components.application.uc_request import GenericUseCaseRequest
from components.application.uc_response import GenericUseCaseResponse


class UseCaseBase(t.Protocol):
    @abstractmethod
    async def execute(
        self, request: GenericUseCaseRequest
    ) -> GenericUseCaseResponse[t.Any]:
        ...
