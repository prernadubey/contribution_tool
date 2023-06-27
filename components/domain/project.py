import typing as t
from dataclasses import dataclass


@dataclass(frozen=True)
class Project:
    """Class representing User model."""

    id: int
    name: str
    type: str
    locations: t.List[str]
