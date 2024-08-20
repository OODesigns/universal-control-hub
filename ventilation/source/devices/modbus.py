from abc import ABC, abstractmethod
from enum import Enum
from devices.device_factory import DeviceFactory

class ModbusMode(Enum):
    TCP = 1
    RTU = 2

class ParityType(Enum):
    NONE = 0
    EVEN = 1
    ODD = 2

class ModbusInterface(ABC):
    def __init__(self, coil_size, discrete_input_size, input_register_size, holding_register_size):
        self.coil_size = coil_size
        self.discrete_input_size = discrete_input_size
        self.input_register_size = input_register_size
        self.holding_register_size = holding_register_size

class ModbusTCPInterface(ModbusInterface):
    @abstractmethod
    def connect_tcp(self, ip_address:str, port:int, timeout:int):
        pass

class ModbusRTUInterface(ModbusInterface):
    @abstractmethod
    def connect_rtu(self, baud_rate:int, parity:ParityType, stop_bits:int, timeout:int):
        pass

@DeviceFactory.register_dependency('modbus_tcp')
class ModbusTCP(ModbusTCPInterface):
    def __init__(self, ip_address, port=502, timeout=1, coil_size=25, discrete_input_size=72, input_register_size=51, holding_register_size=182):
        super().__init__(coil_size, discrete_input_size, input_register_size, holding_register_size)
        self.ip_address = ip_address
        self.port = port
        self.timeout = timeout
        self.connect_tcp(ip_address, port, timeout)

    def connect_tcp(self, ip_address, port, timeout):
        # Logic to initialize a Modbus TCP connection
        print(f"Connecting via Modbus TCP to {ip_address}:{port} with timeout {timeout}s")

    def read(self, address, count):
        # Implement the read functionality for TCP
        pass

    def write(self, address, value):
        # Implement the write functionality for TCP
        pass

@DeviceFactory.register_dependency('modbus_rtu')
class ModbusRTU(ModbusRTUInterface):
    def __init__(self, baudrate=9600, parity='N', stopbits=1, timeout=1, coil_size=25, discrete_input_size=72, input_register_size=51, holding_register_size=182):
        super().__init__(coil_size, discrete_input_size, input_register_size, holding_register_size)
        self.baudrate = baudrate
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout
        self.connect_rtu(baudrate, parity, stopbits, timeout)

    def connect_rtu(self, baudrate, parity, stopbits, timeout):
        # Logic to initialize a Modbus RTU connection
        print(f"Connecting via Modbus RTU with baudrate {baudrate}, parity {parity}, stopbits {stopbits}, timeout {timeout}s")

    def read(self, address, count):
        # Implement the read functionality for RTU
        pass

    def write(self, address, value):
        # Implement the write functionality for RTU
        pass

class ModbusFactory:
    @staticmethod
    def create_modbus(mode: ModbusMode, coil_size=25, discrete_input_size=72, input_register_size=51, holding_register_size=182, **kwargs):
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
                port=kwargs.get('port', 502),
                timeout=kwargs.get('timeout', 1),
                coil_size=coil_size,
                discrete_input_size=discrete_input_size,
                input_register_size=input_register_size,
                holding_register_size=holding_register_size
            )
        elif mode == ModbusMode.RTU:
            return ModbusRTU(
                baudrate=kwargs.get('baudrate', 9600),
                parity=kwargs.get('parity', 'N'),
                stopbits=kwargs.get('stopbits', 1),
                timeout=kwargs.get('timeout', 1),
                coil_size=coil_size,
                discrete_input_size=discrete_input_size,
                input_register_size=input_register_size,
                holding_register_size=holding_register_size
            )
        else:
            raise ValueError("Unsupported mode. Use ModbusMode.TCP or ModbusMode.RTU.")

# Example usage:
# modbus_tcp = ModbusFactory.create_modbus(mode=ModbusMode.TCP, ip_address='192.168.1.10', coil_size=25, discrete_input_size=72, input_register_size=51, holding_register_size=182)
# modbus_rtu = ModbusFactory.create_modbus(mode=ModbusMode.RTU, baudrate=115200, parity='E', coil_size=25, discrete_input_size=72, input_register_size=51, holding_register_size=182)
