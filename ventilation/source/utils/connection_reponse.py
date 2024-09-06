from dataclasses import dataclass

from utils.operation_response import OperationResponse

@dataclass(frozen=True)
class ConnectionResponse(OperationResponse):
    pass
