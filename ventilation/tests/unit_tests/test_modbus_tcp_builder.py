import unittest
from unittest.mock import patch

from modbus.modbus import ModbusData
from modbus.modbus_builder_client import ModbusBuilderClient
from modbus.modbus_tcp_builder import ModbusTCPBuilder
from modbus.tcp_values import IPAddress, Port
from utils.operation_response import OperationResponse


# Mock Modbus client class for testing
class MockModbusClient(ModbusBuilderClient):
    async def connect(self) -> OperationResponse:
        pass

    def disconnect(self) -> OperationResponse:
        pass

    async def read(self) -> ModbusData:
        pass

    def __init__(self, builder):
        self.builder = builder

class TestModbusTCPBuilder(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Register the mock Modbus client for TCP
        ModbusTCPBuilder.register_modbus(MockModbusClient)

    def test_default_initialization(self):
        builder = ModbusTCPBuilder()
        self.assertIsNone(builder.ip_address)
        self.assertIsNone(builder.port)

    def test_set_ip_address(self):
        builder = ModbusTCPBuilder()
        ip = IPAddress('192.168.1.1')
        builder.set_ip_address(ip)
        self.assertEqual(builder.ip_address, ip)

    def test_set_port(self):
        builder = ModbusTCPBuilder()
        port = Port(502)
        builder.set_port(port)
        self.assertEqual(builder.port, port)

    def test_invalid_ip_address(self):
        builder = ModbusTCPBuilder()
        with self.assertRaises(AssertionError):  # Invalid IP format
            # noinspection PyTypeChecker
            builder.set_ip_address("invalid_ip")

    def test_invalid_port(self):
        builder = ModbusTCPBuilder()
        with self.assertRaises(AssertionError):  # Invalid port range
            # noinspection PyTypeChecker
            builder.set_port(123456)

    def test_build_with_valid_ip_and_port(self):
        builder = ModbusTCPBuilder()
        builder.set_ip_address(IPAddress('192.168.1.1')).set_port(Port(502))

        with patch.object(MockModbusClient, '__init__', return_value=None) as mock_init:
            modbus_client = builder.build()
            mock_init.assert_called_once_with(builder)
            self.assertIsInstance(modbus_client, MockModbusClient)

    def test_build_without_ip_address(self):
        builder = ModbusTCPBuilder()
        builder.set_port(Port(502))
        with self.assertRaises(AssertionError):  # IP address is not set
            builder.build()

    def test_build_without_port(self):
        builder = ModbusTCPBuilder()
        builder.set_ip_address(IPAddress('192.168.1.1'))
        with self.assertRaises(AssertionError):  # Port is not set
            builder.build()

if __name__ == '__main__':
    unittest.main()
