import datetime
import typing as t
from uuid import UUID

from pydantic import BaseModel, Field

from components.domain.enums import (
    CompensationRequestStatuses,
    TrainerEmploymentType,
    TrainerLevel,
    TrainingTypes,
    UserRole,
)


class BaseRequestsResponse(BaseModel):
    class Config:
        allow_population_by_field_name = True


class ProjectSchema(BaseRequestsResponse):
    """Class representing User model."""

    id: int = Field(..., alias="ID")
    name: str
    type: str
    locations: t.List[str]


class UserSchema(BaseRequestsResponse):
    """Class representing User model."""

    id: int = Field(..., alias="ID")
    name: str
    surname: str
    email: str
    role: UserRole


class TrainerSchema(BaseRequestsResponse):
    """Class representing Trainer model."""

    id: str = Field(..., alias="ID")
    name: str
    surname: str
    email: str
    role: UserRole
    level: TrainerLevel
    employment_type: TrainerEmploymentType


class ActivityTypeSchema(BaseRequestsResponse):
    """Class representing User model."""

    id: int = Field(..., alias="ID")
    name: str


class CompensationRequestSchema(BaseRequestsResponse):
    id: UUID = Field(..., alias="ID")
    status: CompensationRequestStatuses
    trainer: TrainerSchema
    project: ProjectSchema
    training_type: TrainingTypes = Field(..., alias="trainingType")
    created_at_ts: int = Field(..., alias="createdAtTs")
    created_by: UserSchema = Field(..., alias="createdBy")
    request_initiator: t.Optional[UserSchema] = Field(..., alias="requestInitiator")
    activity_date: datetime.date = Field(..., alias="activityDate")
    activity_type: str = Field(..., alias="activityType")
    course_id: str = Field(..., alias="courseID")
    rd_point: str = Field(..., alias="rdPoint")
    is_rewarded: bool = Field(..., alias="isRewarded")
