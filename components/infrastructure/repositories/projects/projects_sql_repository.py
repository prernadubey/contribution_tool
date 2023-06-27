import typing as t

from sqlalchemy import select
from sqlalchemy.orm import Session

from components.domain.project import Project
from components.domain.repository_interfaces.projects_interface import (
    ProjectsRepositoryProtocol,
)
from components.infrastructure.clients.db.db_models import (
    LocationsDB,
    ProjectsDB,
    ProjectTypesDB,
    project_locations_table,
)


class ProjectsSQLRepository(ProjectsRepositoryProtocol):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_projects(
        self, project_ids: t.Optional[t.List[int]] = None
    ) -> t.List[Project]:
        query = (
            select(
                ProjectsDB.id,
                ProjectsDB.name,
                ProjectTypesDB.name.label("type"),
                LocationsDB.name.label("location"),
            )
            .join(
                ProjectTypesDB,
                ProjectTypesDB.id == ProjectsDB.type_id,
            )
            .join(
                project_locations_table,
                project_locations_table.c.project_id == ProjectsDB.id,
            )
            .join(LocationsDB, project_locations_table.c.location_id == LocationsDB.id)
        )

        if project_ids:
            query = query.filter(ProjectsDB.id.in_(project_ids))

        query_result = await self.db_session.execute(query)  # type: ignore
        result = query_result.fetchall()

        id_to_project = {}
        for r in result:
            if r.id not in id_to_project:
                id_to_project[r.id] = Project(
                    id=r.id,
                    name=r.name,
                    type=r.type,
                    locations=[r.location],
                )
            else:
                id_to_project[r.id].locations.append(r.location)
        return list(id_to_project.values())
