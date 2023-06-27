from abc import abstractmethod
from typing import Protocol

from components.domain.application_status import ApplicationStatus


class ApplicationRepositoryProtocol(Protocol):
    @abstractmethod
    async def get_application_status(self) -> ApplicationStatus:
        ...

    @abstractmethod
    async def turn_on_maintenance_mode(self) -> None:
        ...

    @abstractmethod
    async def turn_off_maintenance_mode(self) -> None:
        ...
