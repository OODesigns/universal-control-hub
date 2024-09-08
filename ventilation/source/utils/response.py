from dataclasses import dataclass
from typing import TypeVar, Generic

from utils.status import Status

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
    status: Status
    details: str
    value: T
