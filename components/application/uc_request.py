import typing as t
from dataclasses import dataclass

DataT = t.TypeVar("DataT")


@dataclass(frozen=True)
class GenericUseCaseRequest(t.Generic[DataT]):
    data: DataT
