from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import List
from modbus.modbus_builder import ModbusBuilder
from utils.connection_reponse import ConnectionResponse
from modbus.modbus_values import CoilSize, DiscreteInputSize, InputRegisterSize, HoldingRegisterSize, Timeout, Retries, \
    ReconnectDelayMax, ReconnectDelay
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

@dataclass(frozen=True)
class ModbusInterface(ABC):
    """
    Immutable Modbus Interface initialized using the ModbusBuilder.
    """
    timeout: Timeout = field(init=False)
    retries: Retries = field(init=False)
    reconnect_delay_max: ReconnectDelayMax = field(init=False)
    reconnect_delay: ReconnectDelay = field(init=False)
    coil_size: CoilSize = field(init=False)
    discrete_input_size: DiscreteInputSize = field(init=False)
    input_register_size: InputRegisterSize = field(init=False)
    holding_register_size: HoldingRegisterSize = field(init=False)

    def __init__(self, builder: ModbusBuilder):
        """
        initialize fields using a ModbusBuilder.
        Extracts values from the builder and assigns them to the instance.
        """
        # Dynamically assign values from the builder to the fields
        object.__setattr__(self, 'timeout', builder.timeout)
        object.__setattr__(self, 'retries', builder.retries)
        object.__setattr__(self, 'reconnect_delay_max', builder.reconnect_delay_max)
        object.__setattr__(self, 'reconnect_delay', builder.reconnect_delay)
        object.__setattr__(self, 'coil_size', builder.coil_size)
        object.__setattr__(self, 'discrete_input_size', builder.discrete_input_size)
        object.__setattr__(self, 'input_register_size', builder.input_register_size)
        object.__setattr__(self, 'holding_register_size', builder.holding_register_size)

    @abstractmethod
    async def connect(self) -> ConnectionResponse: #pragma: nocover
        pass

    @abstractmethod
    def disconnect(self) -> ConnectionResponse: #pragma: nocover
        pass

    @abstractmethod
    async def read(self) -> ModbusData: #pragma: nocover
       pass
