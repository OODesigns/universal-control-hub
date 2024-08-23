from abc import ABC, abstractmethod
from enum import Enum
from devices.modbus_builder import ModbusBuilder

MODBUS = 'modbus'

DELAY_MAX = 300.0
RECONNECT_DELAY = 0.1
RETRIES = 3

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

    @abstractmethod
    async def connect(self):
        pass