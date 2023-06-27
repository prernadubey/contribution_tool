import typing as t
from abc import abstractmethod

from components.domain.user import Trainer


class TrainersRepositoryProtocol(t.Protocol):
    @abstractmethod
    async def get_trainers(
        self, trainer_ids: t.Optional[t.List[int]]
    ) -> t.List[Trainer]:
        ...
