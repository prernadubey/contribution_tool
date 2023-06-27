from dataclasses import dataclass


@dataclass
class ApplicationStatus:
    """Class representing application status model."""

    version: str
    app_name: str
    maintenance_mode: bool
