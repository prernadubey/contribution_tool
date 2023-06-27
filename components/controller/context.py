import typing as t
from contextlib import contextmanager
from contextvars import ContextVar, Token
from dataclasses import dataclass


@dataclass(frozen=True)
class RequestContext:
    request_id: t.Optional[str] = None
    instance: t.Optional[str] = None
    service_version: t.Optional[str] = None


DEFAULT_REQUEST_CONTEXT = RequestContext(
    request_id=None,
    instance=None,
    service_version=None,
)
_request_scope_context: ContextVar[RequestContext] = ContextVar(
    "request_context", default=DEFAULT_REQUEST_CONTEXT
)


def get_request_context() -> RequestContext:
    return _request_scope_context.get()


def set_request_context(request_context: RequestContext) -> Token:
    return _request_scope_context.set(request_context)


@contextmanager
def request_cycle_context(state: RequestContext) -> t.Iterator[None]:
    """Creates and resets a starlette-context context.
    Used in the Context and Raw middlewares, but can also be used to create a
    context out of a proper request cycle, such as in unit tests."""
    token: Token = set_request_context(state)
    try:
        yield
    finally:
        _request_scope_context.reset(token)
