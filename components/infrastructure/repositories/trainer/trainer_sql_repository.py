import logging
import typing as t

from sqlalchemy import select
from sqlalchemy.orm import Session

from components.domain.repository_interfaces.trainers_interface import (
    TrainersRepositoryProtocol,
)
from components.domain.user import Trainer
from components.infrastructure.clients.db.db_models import TrainersDB, UsersDB
from components.settings import get_settings

SETTINGS = get_settings()
_logger = logging.getLogger(__name__)


class TrainersSQLRepository(TrainersRepositoryProtocol):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_trainers(
        self, trainer_ids: t.Optional[t.List[int]] = None
    ) -> t.List[Trainer]:
        query = select(
            UsersDB.id,
            UsersDB.name,
            UsersDB.surname,
            UsersDB.email,
            UsersDB.role,
            TrainersDB.trainer_level,
            TrainersDB.employment_type,
        ).join(TrainersDB, UsersDB.id == TrainersDB.user_id)

        if trainer_ids:
            query = query.filter(UsersDB.id.in_(trainer_ids))

        query_result = await self.db_session.execute(query)  # type: ignore
        result = query_result.fetchall()

        return [
            Trainer(
                id=row.id,
                name=row.name,
                surname=row.surname,
                email=row.email,
                role=row.role,
                level=row.trainer_level,
                employment_type=row.employment_type,
            )
            for row in result
        ]
