import typing as t
from dataclasses import dataclass
from enum import Enum

from components.domain.error_codes import DomainErrorCode


class UseCaseResponseStatus(str, Enum):
    SUCCESS = "Success"
    RESOURCE_NOT_FOUND_ERROR = "Resource not found"
    INTERNAL_ERROR = "Internal Service error"
    EXTERNAL_ERROR = "External Service error"


DataT = t.TypeVar("DataT")


@dataclass(frozen=True)
class GenericUseCaseResponse(t.Generic[DataT]):
    data: t.Optional[DataT]
    status: UseCaseResponseStatus
    error_detail: t.Optional[str]
    code: t.Optional[DomainErrorCode]

    @classmethod
    def build(
        cls,
        *,
        data: t.Optional[DataT] = None,
        status: UseCaseResponseStatus,
        error_detail: t.Optional[str] = None,
        code: t.Optional[DomainErrorCode] = None,
    ) -> "GenericUseCaseResponse":
        """Factory method to build class instance

        Args:
              data: Arbitrary results object.
              error_detail: Detail of error.
              status: Response status.
              code: error code representing domain error.
        Returns:
              class instance
        """
        return cls(data=data, status=status, error_detail=error_detail, code=code)


UseCaseErrorResponse = GenericUseCaseResponse[None]
