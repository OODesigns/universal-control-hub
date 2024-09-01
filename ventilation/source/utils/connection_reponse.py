from dataclasses import dataclass
from enum import Enum


class ConnectionStatus(Enum):
    OK = "OK"
    EXCEPTION = "EXCEPTION"
    FAILED = "FAILED"

@dataclass(frozen=True)
class ConnectionResponse:
    status: ConnectionStatus
    details: str