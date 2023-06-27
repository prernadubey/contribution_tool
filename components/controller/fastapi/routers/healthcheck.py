from fastapi import APIRouter
from starlette import status
from starlette.responses import JSONResponse

healthcheck_router = APIRouter(prefix="/healthcheck", tags=["healthcheck"])


@healthcheck_router.get(
    "",
    response_model=str,
    response_description="The service is alive",
)
def liveness() -> JSONResponse:
    """Check if the service is running.
    This is intended to be used for a Kubernetes liveness probe. It is generally not to be used
    of this service.
    """

    return JSONResponse(status_code=status.HTTP_200_OK, content="Alive")
