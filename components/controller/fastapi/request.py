from pydantic import BaseModel, Extra


class RequestBaseModel(BaseModel):
    """Base Request model."""

    class Config:
        extra = Extra.forbid
        allow_mutation = False
