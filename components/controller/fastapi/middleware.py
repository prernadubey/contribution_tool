import json
import typing as t
import uuid

from starlette.datastructures import MutableHeaders
from starlette.requests import Request as StarletteRequest
from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from components.controller.context import RequestContext, request_cycle_context
from components.controller.fastapi import module_logger
from components.controller.fastapi.default_headers import DefaultHeaders
from components.controller.fastapi.response import ErrorResponse, ErrorResponseDetail
from components.exceptions import get_clean_error_message, get_traceback_struct
from components.settings import get_settings

SETTINGS = get_settings()


async def catch_exceptions_middleware(request: StarletteRequest, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as exc:
        traceback_struct: t.List[t.Dict[t.Any, t.Any]] = get_traceback_struct(exc) or []
        module_logger.error(f"{str(exc)}. trace: {traceback_struct}")

        error_resp = ErrorResponse.build_from_error(
            exc, custom_detail=ErrorResponseDetail.UNEXPECTED_ERROR
        )
        return JSONResponse(
            json.loads(get_clean_error_message(error_resp.json())),
            status_code=error_resp.status,
        )


class CustomMiddleware:
    def __init__(
        self,
        app: ASGIApp,
    ) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ["http", "websocket"]:
            await self.app(scope, receive, send)
            return

        request = StarletteRequest(scope)

        request_id_value: t.Optional[str] = request.headers.get(
            DefaultHeaders.request_id, None
        )
        if not request_id_value:
            request_id_value = uuid.uuid4().hex

        service_version_value: t.Optional[str] = (
            SETTINGS.service_version
            if SETTINGS.service_version != "NO-VERSION"
            else None
        )

        _headers: MutableHeaders = MutableHeaders(scope=scope)
        _headers[DefaultHeaders.request_id] = request_id_value or ""
        _headers[DefaultHeaders.service_version] = service_version_value or ""

        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                headers.append(DefaultHeaders.request_id, request_id_value or "")
                headers.append(
                    DefaultHeaders.service_version, service_version_value or ""
                )

            await send(message)

        request_context = RequestContext(
            request_id=request_id_value,
            instance=request.scope.get("path", ""),
            service_version=service_version_value,
        )
        with request_cycle_context(state=request_context):
            await self.app(scope, receive, send_wrapper)
