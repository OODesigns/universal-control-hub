from modbus.modbus_builder import ModbusBuilder
from modbus.modbus_rtu import ParityType, ModbusRTU
from utils.rtu_values import BaudRate, StopBits, SerialPort

class ModbusRTUBuilder(ModbusBuilder):
    def __init__(self, builder: ModbusBuilder = None):
        super().__init__(builder)
        self._baud_rate = None
        self._parity = None
        self._stop_bits = None
        self._serial_port = None

    # Properties with getters
    @property
    def baud_rate(self) -> BaudRate:
        return self._baud_rate

    @property
    def parity(self) -> ParityType:
        return self._parity

    @property
    def stop_bits(self) -> StopBits:
        return self._stop_bits

    @property
    def serial_port(self) -> SerialPort:
        return self._serial_port

    # Setter methods with validation
    def set_baud_rate(self, baud_rate: BaudRate):
        if not isinstance(baud_rate, BaudRate):
            raise ValueError("Invalid baud rate")
        self._baud_rate = baud_rate
        return self

    def set_parity(self, parity: ParityType):
        if not isinstance(parity, ParityType):
            raise ValueError("Invalid parity type")
        self._parity = parity
        return self

    def set_stop_bits(self, stop_bits: StopBits):
        if not isinstance(stop_bits, StopBits):
            raise ValueError("Invalid stop bits")
        self._stop_bits = stop_bits
        return self

    def set_serial_port(self, serial_port: SerialPort):
        if not isinstance(serial_port, SerialPort):
            raise ValueError("Invalid serial port")
        self._serial_port = serial_port
        return self

    def build(self):
        if not self._baud_rate:
            raise ValueError("Baud rate must be set for ModbusRTU")
        if not self._parity:
            raise ValueError("Parity must be set for ModbusRTU")
        if not self._stop_bits:
            raise ValueError("Stop bits must be set for ModbusRTU")
        if not self._serial_port:
            raise ValueError("Serial port must be set for ModbusRTU")
        return ModbusRTU(self)
