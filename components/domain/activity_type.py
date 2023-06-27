from dataclasses import dataclass


@dataclass
class ActivityType:
    """Class representing Activity Types model."""

    id: int
    name: str
