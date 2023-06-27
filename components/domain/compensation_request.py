import datetime
import typing as t
from dataclasses import dataclass
from uuid import UUID

from components.domain.enums import CompensationRequestStatuses, TrainingTypes
from components.domain.project import Project
from components.domain.skill import Skill
from components.domain.user import Trainer, User


@dataclass(frozen=True)
class CompensationRequest:
    """Class representing User model."""

    id: UUID
    status: CompensationRequestStatuses
    created_by: User
    trainer: Trainer
    project: Project
    training_type: TrainingTypes
    request_initiator: t.Optional[User]
    created_at_ts: int
    activity_date: datetime.date
    activity_type: str
    is_rewarded: bool
    course_id: str
    rd_point: float
    skill: Skill
