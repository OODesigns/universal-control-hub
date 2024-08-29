from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import List
from modbus.modbus_builder import ModbusBuilder
from utils.modbus_values import CoilSize, DiscreteInputSize, InputRegisterSize, HoldingRegisterSize
from utils.value import ValidatedResponse

MODBUS = 'modbus'

DELAY_MAX = 300.0
RECONNECT_DELAY = 0.1
RETRIES = 3

@dataclass(frozen=True)
class ModbusData:
    _input_register: ValidatedResponse
    _holding_register: ValidatedResponse
    _discrete_inputs: ValidatedResponse
    _coils: ValidatedResponse

    @property
    def input_register(self) -> List[int]:
        return self._input_register.value

    @property
    def holding_register(self) -> List[int]:
        return self._holding_register.value

    @property
    def discrete_inputs(self) -> List[bool]:
        return self._discrete_inputs.value

    @property
    def coils(self) -> List[bool]:
        return self._coils.value


class ModbusMode(Enum):
    TCP = 1
    RTU = 2

class ModbusInterface(ABC):
    def __init__(self, builder: ModbusBuilder):
        # Initialize using the builder
        self._timeout = builder.timeout
        self._retries = builder.retries
        self._reconnect_delay_max = builder.reconnect_delay_max
        self._reconnect_delay = builder.reconnect_delay
        self._coil_size = builder.coil_size
        self._discrete_input_size = builder.discrete_input_size
        self._input_register_size = builder.input_register_size
        self._holding_register_size = builder.holding_register_size

    @property
    def coil_size(self) -> CoilSize:
        return self._coil_size

    @property
    def discrete_input_size(self) -> DiscreteInputSize:
        return self._discrete_input_size

    @property
    def input_register_size(self) -> InputRegisterSize:
        return self._input_register_size

    @property
    def holding_register_size(self) -> HoldingRegisterSize:
        return self._holding_register_size

    @abstractmethod
    async def connect(self) -> ValidatedResponse:
        pass

    @abstractmethod
    def disconnect(self) -> ValidatedResponse:
        pass

    @abstractmethod
    async def read(self) -> ModbusData:
        pass