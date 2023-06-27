from components.domain.repository_interfaces.activity_types_interface import (
    ActivityTypesRepositoryProtocol,
)
from components.domain.repository_interfaces.trainers_interface import (
    TrainersRepositoryProtocol,
)
from components.infrastructure.clients.db.create_session import get_session
from components.infrastructure.repositories.activity_types.activity_types_sql_repository import (
    ActivityTypesSQLRepository,
)
from components.infrastructure.repositories.application_status.application_status_local_repository import (
    ApplicationLocalRepository,
)
from components.infrastructure.repositories.application_status.interface import (
    ApplicationRepositoryProtocol,
)
from components.infrastructure.repositories.compensation_requests.compensation_requests_sql_repository import (
    CompensationRequestsRepositoryProtocol,
    CompensationRequestsSQLRepository,
)
from components.infrastructure.repositories.projects.projects_sql_repository import (
    ProjectsRepositoryProtocol,
    ProjectsSQLRepository,
)
from components.infrastructure.repositories.trainer.trainer_sql_repository import (
    TrainersSQLRepository,
)
from components.infrastructure.repositories.users.users_sql_repository import (
    UsersRepositoryProtocol,
    UsersSQLRepository,
)
from components.settings import get_settings

SETTINGS = get_settings()


async def get_application_repository() -> ApplicationRepositoryProtocol:
    return ApplicationLocalRepository(SETTINGS.maintenance_mode_status_filename)


async def get_activity_types_repository() -> ActivityTypesRepositoryProtocol:
    async with get_session() as session:
        async with session.begin():
            return ActivityTypesSQLRepository(session)


async def get_compensation_requests_repository() -> CompensationRequestsRepositoryProtocol:
    async with get_session() as session:
        async with session.begin():
            return CompensationRequestsSQLRepository(session)


async def get_users_repository() -> UsersRepositoryProtocol:
    async with get_session() as session:
        async with session.begin():
            return UsersSQLRepository(session)


async def get_projects_repository() -> ProjectsRepositoryProtocol:
    async with get_session() as session:
        async with session.begin():
            return ProjectsSQLRepository(session)


async def get_trainers_repository() -> TrainersRepositoryProtocol:
    async with get_session() as session:
        async with session.begin():
            return TrainersSQLRepository(session)
