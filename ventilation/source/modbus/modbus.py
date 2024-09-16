from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
from utils.operation_response import OperationResponse
from utils.response import Response

MODBUS = 'modbus'

DELAY_MAX = 300.0
RECONNECT_DELAY = 0.1
RETRIES = 3

@dataclass(frozen=True)
class ModbusData:
    input_register: Response[List[int]]
    holding_register: Response[List[int]]
    discrete_inputs: Response[List[bool]]
    coils: Response[List[bool]]

class ModbusInterface(ABC):
    @abstractmethod
    async def connect(self) -> OperationResponse: #pragma: nocover
        pass

    @abstractmethod
    def disconnect(self) -> OperationResponse: #pragma: nocover
        pass

    @abstractmethod
    async def read(self) -> ModbusData: #pragma: nocover
       pass
