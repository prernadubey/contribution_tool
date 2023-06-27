import typing as t
from abc import abstractmethod

from components.domain.activity_type import ActivityType


class ActivityTypesRepositoryProtocol(t.Protocol):
    @abstractmethod
    async def get_activity_types(self) -> t.List[ActivityType]:
        ...
