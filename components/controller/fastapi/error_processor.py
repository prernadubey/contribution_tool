import json
import typing as t

from starlette.responses import JSONResponse

from components.application.uc_response import (
    GenericUseCaseResponse,
    UseCaseErrorResponse,
    UseCaseResponseStatus,
)
from components.controller.context import get_request_context
from components.controller.fastapi import module_logger
from components.controller.fastapi.response import (
    ErrorResponse,
    ErrorResponseDetail,
    ErrorResponseTitle,
)
from components.exceptions import get_clean_error_message


def process_controller_error_usecase_response(
    use_case_response: t.Union[UseCaseErrorResponse, GenericUseCaseResponse]
):
    _request_context = get_request_context()

    if use_case_response.status is UseCaseResponseStatus.RESOURCE_NOT_FOUND_ERROR:
        error_resp = ErrorResponse(
            title=ErrorResponseTitle.NOT_FOUND_ERROR_RESPONSE,
            status=404,
            code=use_case_response.code if use_case_response.code else None,
            detail=str(use_case_response.error_detail),
            _request_contex=_request_context,
        )

        module_logger.debug(
            f"Created {UseCaseResponseStatus.RESOURCE_NOT_FOUND_ERROR.value} response"
        )

    elif use_case_response.status is UseCaseResponseStatus.INTERNAL_ERROR:
        error_resp = ErrorResponse(
            title=ErrorResponseTitle.INTERNAL_ERROR_RESPONSE,
            status=500,
            detail=ErrorResponseDetail.INTERNAL_ERROR,
            _request_context=_request_context,
        )

        module_logger.debug(
            f"Created {UseCaseResponseStatus.INTERNAL_ERROR.value} response"
        )

    elif use_case_response.status is UseCaseResponseStatus.EXTERNAL_ERROR:
        error_resp = ErrorResponse(
            title=ErrorResponseTitle.EXTERNAL_ERROR_RESPONSE,
            status=503,
            detail=ErrorResponseDetail.EXTERNAL_ERROR,
            _request_context=_request_context,
        )

        module_logger.debug(
            f"Created {UseCaseResponseStatus.EXTERNAL_ERROR.value} response"
        )

    else:
        error_resp = ErrorResponse(
            title=ErrorResponseTitle.UNEXPECTED_ERROR_RESPONSE,
            detail=ErrorResponseDetail.UNEXPECTED_ERROR,
            status=500,
            _request_context=_request_context,
        )
        module_logger.debug(
            f"Created default response, unknown usecase status {use_case_response.status}"
        )

    return JSONResponse(
        json.loads(get_clean_error_message(error_resp.json())),
        status_code=error_resp.status,
        media_type="application/problem+json",
    )
