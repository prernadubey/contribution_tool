import typing as t
from abc import abstractmethod

from components.domain.project import Project


class ProjectsRepositoryProtocol(t.Protocol):
    @abstractmethod
    async def get_projects(
        self, project_ids: t.Optional[t.List[int]]
    ) -> t.List[Project]:
        ...
