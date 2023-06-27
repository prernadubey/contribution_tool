import logging
import typing as t

from components.application.uc_base import UseCaseBase
from components.application.uc_request import GenericUseCaseRequest
from components.application.uc_response import (
    GenericUseCaseResponse,
    UseCaseErrorResponse,
    UseCaseResponseStatus,
)
from components.domain.activity_type import ActivityType
from components.domain.compensation_request import CompensationRequest
from components.domain.project import Project
from components.domain.repository_interfaces.activity_types_interface import (
    ActivityTypesRepositoryProtocol,
)
from components.domain.repository_interfaces.compensation_requests_interface import (
    CompensationRequestDTO,
    CompensationRequestsRepositoryProtocol,
)
from components.domain.repository_interfaces.projects_interface import (
    ProjectsRepositoryProtocol,
)
from components.domain.repository_interfaces.trainers_interface import (
    TrainersRepositoryProtocol,
)
from components.domain.repository_interfaces.users_interface import (
    UsersRepositoryProtocol,
)
from components.domain.user import Trainer, User

_logger = logging.getLogger(__name__)


UseCaseRequest = GenericUseCaseRequest[None]
UseCaseResponse = GenericUseCaseResponse[t.List[CompensationRequest]]


class GetCompensationRequests(UseCaseBase):
    Request = UseCaseRequest
    Response = UseCaseResponse

    def __init__(
        self,
        activity_types_sql_repository: ActivityTypesRepositoryProtocol,
        projects_sql_repository: ProjectsRepositoryProtocol,
        users_sql_repository: UsersRepositoryProtocol,
        trainers_sql_repository: TrainersRepositoryProtocol,
        compensation_requests_sql_repository: CompensationRequestsRepositoryProtocol,
    ):
        self.project_sql_repository = projects_sql_repository
        self.users_sql_repository = users_sql_repository
        self.trainers_sql_repository = trainers_sql_repository
        self.compensation_requests_sql_repository = compensation_requests_sql_repository
        self.activity_types_sql_repository = activity_types_sql_repository

    async def execute(
        self, request: UseCaseRequest
    ) -> t.Union[UseCaseResponse, UseCaseErrorResponse]:
        _logger.info(
            f"Processing GetCompensationRequests use case with request.data:{request.data}"
        )

        compensation_requests: t.List[
            CompensationRequestDTO
        ] = await self.compensation_requests_sql_repository.get_compensation_requests()

        user_ids = set()
        trainer_ids = set()
        project_ids = set()
        for r in compensation_requests:
            user_ids.add(r.created_by_id)
            if r.request_initiator_id:
                user_ids.add(r.request_initiator_id)
            trainer_ids.add(r.trainer_id)
            project_ids.add(r.project_id)

        users: t.List[User] = await self.users_sql_repository.get_users(
            user_ids=list(user_ids)
        )
        trainers: t.List[Trainer] = await self.trainers_sql_repository.get_trainers(
            trainer_ids=list(trainer_ids)
        )
        projects: t.List[Project] = await self.project_sql_repository.get_projects(
            project_ids=list(project_ids)
        )
        activity_types: t.List[
            ActivityType
        ] = await self.activity_types_sql_repository.get_activity_types()

        project_id_to_project: t.Dict[int, Project] = {
            project.id: project for project in projects
        }

        trainer_id_to_trainer: t.Dict[int, Trainer] = {
            trainer.id: trainer for trainer in trainers
        }

        activity_type_id_to_name: t.Dict[int, str] = {
            activity_type.id: activity_type.name for activity_type in activity_types
        }

        user_id_to_user: t.Dict[int, User] = {user.id: user for user in users}
        result = []
        for r in compensation_requests:
            result.append(
                CompensationRequest(
                    id=r.id,
                    status=r.status,
                    created_by=user_id_to_user[r.created_by_id],
                    trainer=trainer_id_to_trainer[r.trainer_id],
                    project=project_id_to_project[r.project_id],
                    training_type=r.training_type,
                    request_initiator=user_id_to_user[r.request_initiator_id]
                    if r.request_initiator_id
                    else None,
                    created_at_ts=r.created_at_ts,
                    activity_date=r.activity_date,
                    activity_type=activity_type_id_to_name[r.activity_type_id],
                    is_rewarded=r.is_rewarded,
                    course_id=r.course_id,
                    rd_point=r.rd_point,
                    skill=r.skill,
                )
            )

        return self.Response.build(status=UseCaseResponseStatus.SUCCESS, data=result)
