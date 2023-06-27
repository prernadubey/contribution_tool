import logging

from fastapi import Depends, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware

import components.controller.fastapi.response as resp
from components.controller.custom_logging import configure_logging
from components.controller.fastapi.default_headers import CommonHeaderParams
from components.controller.fastapi.fastapi_error_handlers import (
    handle_starlette_http_error,
    handle_validation_error,
)
from components.controller.fastapi.middleware import (
    CustomMiddleware,
    catch_exceptions_middleware,
)
from components.controller.fastapi.routers import home_router
from components.settings import get_settings

SETTINGS = get_settings()
_logger = logging.getLogger(__name__)
origins = [
    "http://localhost",
    "http://localhost:3000",
]


def create_component(middleware_enabled: bool = True) -> FastAPI:
    """
    Bootstrap instance of a FastAPI component

    :param middleware_enabled: True to enable middleware when running the service, False otherwise.
    """
    component = FastAPI(
        dependencies=[Depends(CommonHeaderParams)],
        version=SETTINGS.service_version,
        responses={
            **resp.response_422,
            **resp.response_500,
            **resp.response_503,
        },
    )

    # configure component and core libraries
    _configure_error_handlers(component)
    _configure_logging()
    _configure_routers(component)

    if middleware_enabled:
        _configure_middlewares(component)

    return component


def _configure_logging() -> None:
    """Configure logging"""

    configure_logging(
        level=SETTINGS.log_level,
    )


def _configure_routers(component: FastAPI) -> None:
    """Register the routers on the component.
    Routers are objects that map url routes to our python functions"""
    component.include_router(home_router)


def _configure_middlewares(component: FastAPI) -> None:
    component.add_middleware(BaseHTTPMiddleware, dispatch=catch_exceptions_middleware)
    component.add_middleware(CustomMiddleware)
    component.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def _configure_error_handlers(component: FastAPI) -> None:
    component.add_exception_handler(RequestValidationError, handle_validation_error)
    component.add_exception_handler(StarletteHTTPException, handle_starlette_http_error)
