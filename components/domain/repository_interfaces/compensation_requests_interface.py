import datetime
import typing as t
from abc import abstractmethod
from dataclasses import dataclass
from uuid import UUID

from components.domain.enums import CompensationRequestStatuses, TrainingTypes
from components.domain.skill import Skill


@dataclass(frozen=True)
class CompensationRequestDTO:
    """Class representing partially instantiated CompensationRequest model."""

    id: UUID
    status: CompensationRequestStatuses
    request_initiator_id: int
    trainer_id: int
    project_id: int
    training_type: TrainingTypes
    created_by_id: int
    created_at_ts: int
    activity_date: datetime.date
    activity_type_id: int
    is_rewarded: bool
    course_id: str
    rd_point: float
    skill: Skill


class CompensationRequestsRepositoryProtocol(t.Protocol):
    @abstractmethod
    async def get_compensation_requests(self) -> t.List[CompensationRequestDTO]:
        ...
