from dataclasses import dataclass

from components.domain.enums import TrainerEmploymentType, TrainerLevel, UserRole


@dataclass
class User:
    """Class representing User model."""

    id: int
    name: str
    surname: str
    email: str
    role: UserRole


@dataclass
class Trainer(User):
    """Class representing Trainer model."""

    level: TrainerLevel
    employment_type: TrainerEmploymentType
