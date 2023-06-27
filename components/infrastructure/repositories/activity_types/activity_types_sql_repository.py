import logging
import typing as t

from sqlalchemy import select
from sqlalchemy.orm import Session

from components.domain.activity_type import ActivityType
from components.domain.repository_interfaces.activity_types_interface import (
    ActivityTypesRepositoryProtocol,
)
from components.infrastructure.clients.db.db_models import ActivityTypesDB
from components.settings import get_settings

SETTINGS = get_settings()
_logger = logging.getLogger(__name__)


class ActivityTypesSQLRepository(ActivityTypesRepositoryProtocol):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_activity_types(self) -> t.List[ActivityType]:
        query = select(ActivityTypesDB.id, ActivityTypesDB.name)
        query_result = await self.db_session.execute(query)  # type: ignore
        result = query_result.fetchall()
        return [ActivityType(id=r.id, name=r.name) for r in result]
