from fastapi import APIRouter

from components.controller.fastapi.routers.v1.activity_types import (
    router as activity_types_router,
)
from components.controller.fastapi.routers.v1.application_status import (
    router as application_status_router,
)
from components.controller.fastapi.routers.v1.compensation_requests import (
    router as compensation_requests_router,
)
from components.controller.fastapi.routers.v1.current_user import (
    router as current_user_router,
)

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(application_status_router)
v1_router.include_router(activity_types_router)
v1_router.include_router(current_user_router)
v1_router.include_router(compensation_requests_router)
