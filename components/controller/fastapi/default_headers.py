from fastapi import Header


class DefaultHeaders:
    request_id = "X-Request-ID"
    service_version = "X-Service-Version"


class CommonHeaderParams:
    def __init__(
        self,
        request_id: str = Header(None, alias=DefaultHeaders.request_id),
    ):
        """Class used to define default headers as fastapi dependencies"""
