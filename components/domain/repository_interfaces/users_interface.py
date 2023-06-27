import typing as t
from abc import abstractmethod

from components.domain.user import User


class UsersRepositoryProtocol(t.Protocol):
    @abstractmethod
    async def get_users(self, user_ids: t.Optional[t.List[int]]) -> t.List[User]:
        ...

    @abstractmethod
    async def get_user(self, user_id: int) -> t.Optional[User]:
        ...
