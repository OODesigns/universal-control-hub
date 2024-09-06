from dataclasses import dataclass
from enum import Enum


class OperationStatus(Enum):
    OK = "OK"
    EXCEPTION = "EXCEPTION"
    FAILED = "FAILED"


@dataclass(frozen=True)
class OperationResponse:
    status: OperationStatus
    details: str