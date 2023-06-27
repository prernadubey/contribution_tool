import uuid

from sqlalchemy import (
    TIMESTAMP,
    UUID,
    BigInteger,
    Boolean,
    CheckConstraint,
    Column,
    Date,
)
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Float, ForeignKey, Integer, String, Table

from components.domain.enums import (
    CompensationRequestStatuses,
    TrainerEmploymentType,
    TrainingTypes,
    UserRole,
)
from components.infrastructure.clients.db.session import SQLAlchemyBase


class ProjectTypesDB(SQLAlchemyBase):
    __tablename__ = "project_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)


class ProjectsDB(SQLAlchemyBase):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type_id = Column(Integer, ForeignKey("project_types.id"), nullable=False)


class LocationsDB(SQLAlchemyBase):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)


project_locations_table = Table(
    "project_locations",
    SQLAlchemyBase.metadata,
    Column("location_id", ForeignKey("locations.id")),
    Column("project_id", ForeignKey("projects.id")),
)


class UsersDB(SQLAlchemyBase):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole))


class TrainersDB(SQLAlchemyBase):
    __tablename__ = "trainers"

    user_id = Column(
        BigInteger, ForeignKey("users.id"), nullable=False, primary_key=True
    )
    trainer_level = Column(String, nullable=False, primary_key=True)
    employment_type = Column(SQLEnum(TrainerEmploymentType))
    __table_args__ = (
        CheckConstraint(trainer_level.in_(["R1", "R2", "R3", "R4", "R5"])),
    )


class ActivityTypesDB(SQLAlchemyBase):
    __tablename__ = "activity_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)


class SkillsDB(SQLAlchemyBase):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)


class CompensationRequestsDB(SQLAlchemyBase):
    __tablename__ = "compensation_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    status = Column(SQLEnum(CompensationRequestStatuses))
    created_at = Column(TIMESTAMP, nullable=False)
    created_by_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    trainer_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    training_type = Column(SQLEnum(TrainingTypes))
    course_id = Column(String, nullable=False)
    activity_date = Column(Date, nullable=False)
    activity_type_id = Column(Integer, ForeignKey("activity_types.id"), nullable=False)
    is_rewarded = Column(Boolean, nullable=False)
    request_initiator_id = Column(BigInteger, ForeignKey("users.id"), nullable=True)
    rd_point = Column(Float, nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
