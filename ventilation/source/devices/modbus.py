from abc import ABC, abstractmethod
from enum import Enum
from devices.device_factory import DeviceFactory
from utils.rtu_values import BaudRate, StopBits
from utils.tcp_values import IPAddress, Timeout, Port


class ModbusMode(Enum):
    TCP = 1
    RTU = 2

class ParityType(Enum):
    NONE = 0
    EVEN = 1
    ODD = 2

class ModbusInterface(ABC):
    def __init__(self, coil_size: int, discrete_input_size: int, input_register_size: int, holding_register_size: int):
        # Validate that sizes are integers and positive
        self._coil_size = self.validate_size(coil_size, "coil_size")
        self._discrete_input_size = self.validate_size(discrete_input_size, "discrete_input_size")
        self._input_register_size = self.validate_size(input_register_size, "input_register_size")
        self._holding_register_size = self.validate_size(holding_register_size, "holding_register_size")

    @classmethod
    def validate_size(cls,value: int, name: str) -> int:
        if not isinstance(value, int) or value < 0:
            raise ValueError(f"{name} must be a non-negative integer, got {value}")
        return value

class ModbusTCPInterface(ModbusInterface):
    @abstractmethod
    def connect_tcp(self, ip_address: IPAddress, port: Port, timeout: Timeout):
        pass

class ModbusRTUInterface(ModbusInterface):
    @abstractmethod
    def connect_rtu(self, baud_rate: BaudRate, parity: ParityType, stop_bits: StopBits):
        pass

@DeviceFactory.register_dependency('modbus_tcp')
class ModbusTCP(ModbusTCPInterface):
    def __init__(self, ip_address, port:Port, timeout:Timeout, coil_size:int, discrete_input_size:int,
                 input_register_size:int, holding_register_size:int):
        super().__init__(coil_size, discrete_input_size, input_register_size, holding_register_size)
        self._ip_address = ip_address
        self._port = port
        self._timeout = timeout
        self.connect_tcp(self._ip_address, self._port, self._timeout)

    def connect_tcp(self, ip_address: IPAddress, port: Port, timeout: Timeout):
        # Logic to initialize a Modbus TCP connection
        print(f"Connecting via Modbus TCP to {ip_address.value}:{port.value} with timeout {timeout.value}s")

    def read(self, address, count):
        # Implement the read functionality for TCP
        pass

    def write(self, address, value):
        # Implement the write functionality for TCP
        pass

@DeviceFactory.register_dependency('modbus_rtu')
class ModbusRTU(ModbusRTUInterface):
    def __init__(self, baud_rate:BaudRate, parity:ParityType, stop_bits:StopBits,
                 coil_size:int, discrete_input_size:int, input_register_size:int, holding_register_size:int):
        super().__init__(coil_size, discrete_input_size, input_register_size, holding_register_size)
        self._baud_rate = baud_rate
        self._parity = parity
        self._stop_bits = stop_bits
        self.connect_rtu(self._baud_rate, self._parity, self._stop_bits)

    def connect_rtu(self, baud_rate: BaudRate, parity: ParityType, stop_bits: StopBits):
        # Logic to initialize a Modbus RTU connection
        print(f"Connecting via Modbus RTU with baud rate {baud_rate.value}, parity {parity.name}, "
              f"stop bits {stop_bits.value}")

    def read(self, address, count):
        # Implement the read functionality for RTU
        pass

    def write(self, address, value):
        # Implement the write functionality for RTU
        pass

class ModbusFactory:
    @classmethod
    def create_modbus(cls, mode: ModbusMode, coil_size:int, discrete_input_size:int,
                      input_register_size:int, holding_register_size:int, **kwargs):
        """
        Factory method to create either a ModbusTCP or ModbusRTU instance.

        :param mode: ModbusMode Enum (TCP or RTU)
        :param coil_size: The size of the coils (single-bit registers)
        :param discrete_input_size: The size of the discrete inputs
        :param input_register_size: The size of the input registers
        :param holding_register_size: The size of the holding registers
        :param kwargs: Additional parameters for the respective mode
        :return: ModbusTCP or ModbusRTU instance
        """
        if mode == ModbusMode.TCP:
            return ModbusTCP(
                ip_address=kwargs.get('ip_address'),
                port=kwargs.get('port'),
                timeout=kwargs.get('timeout'),
                coil_size=coil_size,
                discrete_input_size=discrete_input_size,
                input_register_size=input_register_size,
                holding_register_size=holding_register_size
            )
        elif mode == ModbusMode.RTU:
            return ModbusRTU(
                baud_rate=kwargs.get('baud_rate'),
                parity=kwargs.get('parity'),
                stop_bits=kwargs.get('stop_bits'),
                coil_size=coil_size,
                discrete_input_size=discrete_input_size,
                input_register_size=input_register_size,
                holding_register_size=holding_register_size
            )
        else:
            raise ValueError("Unsupported mode. Use ModbusMode.TCP or ModbusMode.RTU.")
