import json
import typing as t

from starlette.responses import JSONResponse

from components.controller.fastapi import module_logger
from components.controller.fastapi.response import ErrorResponse
from components.exceptions import get_traceback_struct


async def handle_validation_error(_, exc):
    traceback_struct: t.List[t.Dict[t.Any, t.Any]] = get_traceback_struct(exc) or []
    module_logger.error(f"{str(exc)}. trace: {traceback_struct}")

    error_resp = ErrorResponse.build_from_validation_error(exc)
    return JSONResponse(json.loads(error_resp.json()), status_code=error_resp.status)


async def handle_starlette_http_error(_, exc):
    traceback_struct: t.List[t.Dict[t.Any, t.Any]] = get_traceback_struct(exc) or []
    module_logger.error(f"{str(exc)}. trace: {traceback_struct}")

    error_resp = ErrorResponse.build_from_starlette_error(exc)

    return JSONResponse(json.loads(error_resp.json()), status_code=error_resp.status)
