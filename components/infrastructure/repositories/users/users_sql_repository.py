import typing as t

from sqlalchemy import select
from sqlalchemy.orm import Session

from components.domain.repository_interfaces.users_interface import (
    UsersRepositoryProtocol,
)
from components.domain.user import User
from components.infrastructure.clients.db.db_models import UsersDB


class UsersSQLRepository(UsersRepositoryProtocol):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_users(self, user_ids: t.Optional[t.List[int]] = None) -> t.List[User]:
        query = select(
            UsersDB.id, UsersDB.name, UsersDB.surname, UsersDB.email, UsersDB.role
        )

        if user_ids:
            query = query.filter(UsersDB.id.in_(user_ids))

        query_result = await self.db_session.execute(query)  # type: ignore
        result = query_result.fetchall()
        return [
            User(id=r.id, name=r.name, surname=r.surname, email=r.email, role=r.role)
            for r in result
        ]

    async def get_user(self, user_id: int) -> t.Optional[User]:
        query = select(
            UsersDB.id, UsersDB.name, UsersDB.surname, UsersDB.email, UsersDB.role
        ).filter(UsersDB.id == user_id)

        query_result = await self.db_session.execute(query)  # type: ignore
        result = query_result.one_or_none()

        if result:
            return User(
                id=result.id,
                name=result.name,
                surname=result.surname,
                email=result.email,
                role=result.role,
            )
        return None
