from modbus.modbus_client_builder import ModbusClientBuilder
from modbus.rtu_values import BaudRate, StopBits, SerialPort, ParityType
from modbus.modbus import ModbusInterface


class ModbusRTUClientBuilder(ModbusClientBuilder):
    def __init__(self):
        super().__init__()
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
        assert isinstance(baud_rate, BaudRate), "Invalid baud rate"
        self._baud_rate = baud_rate
        return self

    def set_parity(self, parity: ParityType):
        assert isinstance(parity, ParityType), "Invalid parity type"
        self._parity = parity
        return self

    def set_stop_bits(self, stop_bits: StopBits):
        assert isinstance(stop_bits, StopBits), "Invalid stop bits"
        self._stop_bits = stop_bits
        return self

    def set_serial_port(self, serial_port: SerialPort):
        assert isinstance(serial_port, SerialPort), "Invalid serial port"
        self._serial_port = serial_port
        return self

    def build(self) -> ModbusInterface:
        assert self._baud_rate, "Baud rate must be set for ModbusRTU"
        assert self._parity, "Parity must be set for ModbusRTU"
        assert self._stop_bits, "Stop bits must be set for ModbusRTU"
        assert self._serial_port, "Serial port must be set for ModbusRTU"
        return super().build()
