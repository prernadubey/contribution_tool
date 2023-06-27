import logging
import typing as t
from dataclasses import dataclass
from enum import Enum

from pydantic import BaseModel, Extra, ValidationError
from starlette import status
from starlette.exceptions import HTTPException as StarletteHTTPException

from components.application.uc_response import UseCaseResponseStatus
from components.controller.context import RequestContext
from components.domain.error_codes import DomainErrorCode

_logger: logging.Logger = logging.getLogger("ExceptionLogger")


class ErrorResponseTitle(str, Enum):
    """Predefined error titles"""

    INTERNAL_ERROR_RESPONSE = "Internal Service error has occurred"
    EXTERNAL_ERROR_RESPONSE = "External Service error has occurred"
    UNEXPECTED_ERROR_RESPONSE = "An unexpected error has occurred"
    NOT_FOUND_ERROR_RESPONSE = "Cannot find specified resource"
    VALIDATION_ERROR = "A validation error has occurred"


@dataclass(frozen=True)
class ErrorResponseDetail:
    """Predefined error titles"""

    UNEXPECTED_ERROR = "Error happened"
    INTERNAL_ERROR = "Error happened"
    EXTERNAL_ERROR = "Error happened"
    VALIDATION_ERROR = "A validation error has occurred"


class ResponseBaseModel(BaseModel):
    """Base Response model."""

    class Config:
        extra = Extra.forbid
        allow_mutation = False
        allow_population_by_field_name = True


@dataclass(frozen=True)
class InvalidParams:
    """
    Model representing invalid input params"""

    name: str
    reason: str


class ErrorResponse(BaseModel):
    type: t.Optional[str] = "about:blank"
    title: ErrorResponseTitle = (
        ErrorResponseTitle.UNEXPECTED_ERROR_RESPONSE
    )  # A short, human-readable summary of the problem type.
    status: int = 500  # HTTP status code
    detail: t.Optional[
        str
    ] = None  # A human-readable detail specific to this occurrence of error.
    instance: t.Optional[
        str
    ] = None  # A URI reference that identifies the specific occurrence of the problem.
    invalid_params: t.Optional[t.List[InvalidParams]] = None
    code: t.Optional[DomainErrorCode] = None  # Domain error code.
    request_id: t.Optional[str] = None

    def __init__(self, _request_context: t.Optional[RequestContext] = None, **kwargs):
        if _request_context:
            kwargs["request_id"] = _request_context.request_id
            kwargs["instance"] = _request_context.instance
        super().__init__(**kwargs)

    @classmethod
    def build_from_validation_error(
        cls, exc: ValidationError, request_context: t.Optional[RequestContext] = None
    ) -> "ErrorResponse":
        """Factory method that creates instance from ValidationError.

        Returns
            exception (Exception) - exception instance.
        Raises
            ErrorResponse instance of ErrorResponse class.
        """
        invalid_params = [
            {
                "name": "->".join([str(i) for i in e["loc"]]),
                "reason": e["msg"],
            }
            for e in exc.errors()
        ]

        invalid_params_objects = [InvalidParams(**i) for i in invalid_params]

        _logger.error(
            ErrorResponseTitle.VALIDATION_ERROR.value,
            extra={"invalid params": invalid_params},
        )

        return ErrorResponse(
            title=ErrorResponseTitle.VALIDATION_ERROR,
            status=422,
            code=None,
            detail=ErrorResponseDetail.VALIDATION_ERROR,
            invalid_params=invalid_params_objects,
            _request_context=request_context,
        )

    @classmethod
    def build_from_error(
        cls,
        exc: Exception,
        request_context: t.Optional[RequestContext] = None,
        custom_detail: t.Optional[str] = None,
    ) -> "ErrorResponse":
        """Factory method that creates instance from ordinary Exception.

        Returns
            exception (Exception) - exception instance.
        Raises
            ErrorResponse instance of ErrorResponse class.
        """
        http_code = 500
        detail = str(exc) if not custom_detail else custom_detail

        _logger.error(detail)

        return ErrorResponse(
            title=ErrorResponseTitle.UNEXPECTED_ERROR_RESPONSE,
            status=http_code,
            code=None,
            detail=detail,
            _request_context=request_context,
        )

    @classmethod
    def build_from_starlette_error(
        cls,
        exc: StarletteHTTPException,
        request_context: t.Optional[RequestContext] = None,
        custom_detail: t.Optional[str] = None,
    ) -> "ErrorResponse":
        """Factory method that creates instance from ordinary Exception.

        Returns
            exception (Exception) - exception instance.
        Raises
            ErrorResponse instance of ErrorResponse class.
        """
        http_code = exc.status_code
        detail = exc.detail if not custom_detail else custom_detail

        _logger.error(detail)

        return ErrorResponse(
            title=ErrorResponseTitle.UNEXPECTED_ERROR_RESPONSE,
            status=http_code,
            code=None,
            detail=detail,
            _request_context=request_context,
        )


usecase_controller_mapping = {
    UseCaseResponseStatus.SUCCESS: status.HTTP_200_OK,
    UseCaseResponseStatus.RESOURCE_NOT_FOUND_ERROR: status.HTTP_404_NOT_FOUND,
    UseCaseResponseStatus.INTERNAL_ERROR: status.HTTP_500_INTERNAL_SERVER_ERROR,
    UseCaseResponseStatus.EXTERNAL_ERROR: status.HTTP_503_SERVICE_UNAVAILABLE,
}


response_500: t.Mapping[t.Union[int, str], t.Dict[str, t.Any]] = {
    500: {
        "model": ErrorResponse,
        "description": (
            "Something has gone wrong on our end. Please reach out to support team."
        ),
        "content": {
            "application/problem+json": {
                "schema": {"$ref": "#/components/schemas/ErrorResponse"},
                "example": {
                    "type": "about:blank",
                    "title": ErrorResponseTitle.INTERNAL_ERROR_RESPONSE,
                    "status": 500,
                    "detail": ErrorResponseDetail.INTERNAL_ERROR,
                    "instance": None,
                    "invalid_params": None,
                    "code": None,
                    "request_id": "£02bd922b0b440d3a7e842d05d47e203",
                },
            }
        },
    }
}

response_503: t.Mapping[t.Union[int, str], t.Dict[str, t.Any]] = {
    503: {
        "model": ErrorResponse,
        "description": (
            "Something has gone wrong on our end. Please reach out to support team."
        ),
        "content": {
            "application/problem+json": {
                "schema": {"$ref": "#/components/schemas/ErrorResponse"},
                "example": {
                    "type": "about:blank",
                    "title": ErrorResponseTitle.EXTERNAL_ERROR_RESPONSE,
                    "status": 503,
                    "detail": ErrorResponseDetail.EXTERNAL_ERROR,
                    "instance": None,
                    "invalid_params": None,
                    "code": None,
                    "request_id": "£02bd922b0b440d3a7e842d05d47e203",
                },
            }
        },
    }
}


response_404: t.Mapping[t.Union[int, str], t.Dict[str, t.Any]] = {
    404: {
        "model": ErrorResponse,
        "description": ("Resource does not exist"),
        "content": {
            "application/problem+json": {
                "schema": {"$ref": "#/components/schemas/ErrorResponse"},
                "example": {
                    "type": "about:blank",
                    "title": ErrorResponseTitle.NOT_FOUND_ERROR_RESPONSE,
                    "status": 404,
                    "detail": "Cannot find resource with id=1",
                    "instance": None,
                    "invalid_params": "/example/res/1",
                    "code": 1000,
                    "request_id": "£02bd922b0b440d3a7e842d05d47e203",
                },
            }
        },
    }
}

response_422: t.Mapping[t.Union[int, str], t.Dict[str, t.Any]] = {
    422: {
        "model": ErrorResponse,
        "description": ("Validation error "),
        "content": {
            "application/problem+json": {
                "schema": {"$ref": "#/components/schemas/ErrorResponse"},
                "example": {
                    "type": "about:blank",
                    "title": ErrorResponseTitle.VALIDATION_ERROR,
                    "status": 422,
                    "detail": ErrorResponseDetail.VALIDATION_ERROR,
                    "instance": None,
                    "invalid_params": [{"name": "string", "reason": "string"}],
                    "code": None,
                    "request_id": "£02bd922b0b440d3a7e842d05d47e203",
                },
            }
        },
    }
}
