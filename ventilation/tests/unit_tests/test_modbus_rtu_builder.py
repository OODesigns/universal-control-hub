import unittest
from unittest.mock import patch
from modbus.modbus_builder_client import ModbusBuilderClient
from modbus.modus_rtu_client_builder import ModbusRTUClientBuilder
from modbus.rtu_values import BaudRate, StopBits, SerialPort, ParityType
from modbus.modbus_values import Timeout, Retries, ReconnectDelay, ReconnectDelayMax, CoilSize, DiscreteInputSize, InputRegisterSize, HoldingRegisterSize
from modbus.modbus import ModbusData
from utils.operation_response import OperationResponse


# Mock Modbus RTU client class for testing
class MockModbusRTUClient(ModbusBuilderClient):
    async def connect(self) -> OperationResponse:
        pass

    def disconnect(self) -> OperationResponse:
        pass

    async def read(self) -> ModbusData:
        pass

    def __init__(self, builder):
        self.builder = builder

class TestModbusRTUBuilder(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Register the mock Modbus RTU client
        ModbusRTUClientBuilder.register_client(MockModbusRTUClient)

    def test_default_initialization(self):
        builder = ModbusRTUClientBuilder()
        # Ensure all values are None by default
        self.assertIsNone(builder.baud_rate)
        self.assertIsNone(builder.parity)
        self.assertIsNone(builder.stop_bits)
        self.assertIsNone(builder.serial_port)

    def test_set_baud_rate(self):
        builder = ModbusRTUClientBuilder()
        baud_rate = BaudRate(9600)
        builder.set_baud_rate(baud_rate)
        self.assertEqual(builder.baud_rate, baud_rate)

    def test_set_parity(self):
        builder = ModbusRTUClientBuilder()
        parity = ParityType.EVEN
        builder.set_parity(parity)
        self.assertEqual(builder.parity, parity)

    def test_set_stop_bits(self):
        builder = ModbusRTUClientBuilder()
        stop_bits = StopBits(1)
        builder.set_stop_bits(stop_bits)
        self.assertEqual(builder.stop_bits, stop_bits)

    def test_set_serial_port(self):
        builder = ModbusRTUClientBuilder()
        serial_port = SerialPort("COM1")
        builder.set_serial_port(serial_port)
        self.assertEqual(builder.serial_port, serial_port)

    def test_build_with_valid_settings(self):
        builder = ModbusRTUClientBuilder()
        builder.set_baud_rate(BaudRate(9600)) \
            .set_parity(ParityType.EVEN) \
            .set_stop_bits(StopBits(1)) \
            .set_serial_port(SerialPort("COM1")) \
            .set_coil_size(CoilSize(10)) \
            .set_discrete_input_size(DiscreteInputSize(20)) \
            .set_input_register_size(InputRegisterSize(30)) \
            .set_holding_register_size(HoldingRegisterSize(40)) \
            .set_timeout(Timeout(5.0)) \
            .set_reconnect_delay(ReconnectDelay(2.0)) \
            .set_reconnect_delay_max(ReconnectDelayMax(10.0)) \
            .set_retries(Retries(5))

        with patch.object(MockModbusRTUClient, '__init__', return_value=None) as mock_init:
            modbus_rtu = builder.build()
            mock_init.assert_called_once_with(builder)
            self.assertIsInstance(modbus_rtu, MockModbusRTUClient)

    def test_build_without_baud_rate(self):
        builder = ModbusRTUClientBuilder()
        builder.set_parity(ParityType.EVEN).set_stop_bits(StopBits(1)).set_serial_port(SerialPort("COM1"))
        with self.assertRaises(AssertionError):  # Baud rate not set
            builder.build()

    def test_build_without_parity(self):
        builder = ModbusRTUClientBuilder()
        builder.set_baud_rate(BaudRate(9600)).set_stop_bits(StopBits(1)).set_serial_port(SerialPort("COM1"))
        with self.assertRaises(AssertionError):  # Parity not set
            builder.build()

    def test_build_without_stop_bits(self):
        builder = ModbusRTUClientBuilder()
        builder.set_baud_rate(BaudRate(9600)).set_parity(ParityType.EVEN).set_serial_port(SerialPort("COM1"))
        with self.assertRaises(AssertionError):  # Stop bits not set
            builder.build()

    def test_build_without_serial_port(self):
        builder = ModbusRTUClientBuilder()
        builder.set_baud_rate(BaudRate(9600)).set_parity(ParityType.EVEN).set_stop_bits(StopBits(1))
        with self.assertRaises(AssertionError):  # Serial port not set
            builder.build()

    def test_invalid_baud_rate(self):
        builder = ModbusRTUClientBuilder()
        with self.assertRaises(AssertionError):  # Invalid baud rate
            # noinspection PyTypeChecker
            builder.set_baud_rate("invalid_baud_rate")

    def test_invalid_parity(self):
        builder = ModbusRTUClientBuilder()
        with self.assertRaises(AssertionError):  # Invalid parity type
            # noinspection PyTypeChecker
            builder.set_parity("invalid_parity")

    def test_invalid_stop_bits(self):
        builder = ModbusRTUClientBuilder()
        with self.assertRaises(AssertionError):  # Invalid stop bits
            # noinspection PyTypeChecker
            builder.set_stop_bits("invalid_stop_bits")

    def test_invalid_serial_port(self):
        builder = ModbusRTUClientBuilder()
        with self.assertRaises(AssertionError):  # Invalid serial port
            # noinspection PyTypeChecker
            builder.set_serial_port("invalid_serial_port")

if __name__ == '__main__':
    unittest.main()