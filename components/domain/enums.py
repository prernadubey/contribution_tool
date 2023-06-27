from enum import Enum


class UserRole(str, Enum):
    user = "user"
    approver = "approver"
    admin = "admin"


class TrainerLevel(str, Enum):
    R1 = "R1"
    R2 = "R2"
    R3 = "R3"
    R4 = "R4"
    R5 = "R5"


class CompensationRequestStatuses(str, Enum):
    draft = "draft"
    pending = "pending"
    confirmed = "confirmed"
    denied = "denied"


class TrainingTypes(str, Enum):
    internal_training = "internal_training"
    external_training = "external_training"
    other = "other"


class TrainerEmploymentType(str, Enum):
    internal = "internal"
    external = "external"
    subcontractor = "subcontractor"
