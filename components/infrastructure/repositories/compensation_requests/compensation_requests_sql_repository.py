import calendar
import logging
import typing as t

from sqlalchemy import select
from sqlalchemy.orm import Session

from components.domain.repository_interfaces.compensation_requests_interface import (
    CompensationRequestDTO,
    CompensationRequestsRepositoryProtocol,
)
from components.infrastructure.clients.db.db_models import (
    CompensationRequestsDB,
    SkillsDB,
)
from components.settings import get_settings

SETTINGS = get_settings()
_logger = logging.getLogger(__name__)


class CompensationRequestsSQLRepository(CompensationRequestsRepositoryProtocol):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_compensation_requests(self) -> t.List[CompensationRequestDTO]:
        query = select(
            CompensationRequestsDB.id,
            CompensationRequestsDB.status,
            CompensationRequestsDB.request_initiator_id,
            CompensationRequestsDB.trainer_id,
            CompensationRequestsDB.project_id,
            CompensationRequestsDB.training_type,
            CompensationRequestsDB.created_by_id,
            CompensationRequestsDB.created_at,
            CompensationRequestsDB.activity_date,
            CompensationRequestsDB.activity_type_id,
            CompensationRequestsDB.is_rewarded,
            CompensationRequestsDB.course_id,
            CompensationRequestsDB.rd_point,
            SkillsDB.name.label("skill_name"),
        ).join(SkillsDB, CompensationRequestsDB.skill_id == SkillsDB.id)
        query_result = await self.db_session.execute(query)  # type: ignore
        result = query_result.fetchall()
        return [
            CompensationRequestDTO(
                id=row.id,
                status=row.status,
                request_initiator_id=row.request_initiator_id,
                trainer_id=row.trainer_id,
                project_id=row.project_id,
                training_type=row.training_type,
                created_by_id=row.created_by_id,
                created_at_ts=calendar.timegm(row.created_at.utctimetuple()),
                activity_date=row.activity_date,
                activity_type_id=row.activity_type_id,
                is_rewarded=row.is_rewarded,
                course_id=row.course_id,
                rd_point=row.rd_point,
                skill=row.skill_name,
            )
            for row in result
        ]
