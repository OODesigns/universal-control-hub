from enum import Enum
from typing import TypeVar, Generic

from attr import dataclass


class ResponseStatus(Enum):
    """
    Enum to represent the status of a process.
    """
    OK = 0
    EXCEPTION = 1


T = TypeVar('T')


@dataclass(frozen=True)
class Response(Generic[T]):
    """
    Data class to encapsulate the result of a process.

    Attributes:
        status: The status of the response (OK or EXCEPTION).
        details: A message detailing the result of the validation.
        value: The value being validated.
    """
    status: ResponseStatus
    details: str
    value: T
