import unittest
from unittest.mock import patch

from modbus.modbus import ModbusData
from modbus.modbus_builder_client import ModbusBuilderClient
from modbus.modbus_tcp_client_builder import ModbusTCPClientBuilder
from modbus.tcp_values import IPAddress, Port
from modbus.modbus_values import CoilSize, DiscreteInputSize, InputRegisterSize, HoldingRegisterSize, Timeout, ReconnectDelay, ReconnectDelayMax
from utils.operation_response import OperationResponse


# Mock Modbus client class for testing
class MockModbusClient(ModbusBuilderClient):
    async def read(self) -> ModbusData:
        pass

    def disconnect(self) -> OperationResponse:
        pass

    async def connect(self) -> OperationResponse:
        pass

    def __init__(self, builder):
        self.builder = builder

class TestModbusTCPBuilder(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Register the mock Modbus client for TCP
        ModbusTCPClientBuilder.register_client(MockModbusClient)

    @classmethod
    def set_builder_with_required_fields(cls, builder):
        builder.set_ip_address(IPAddress('192.168.1.1'))
        builder.set_port(Port(502))
        builder.set_coil_size(CoilSize(10))
        builder.set_discrete_input_size(DiscreteInputSize(20))
        builder.set_input_register_size(InputRegisterSize(30))
        builder.set_holding_register_size(HoldingRegisterSize(40))
        builder.set_timeout(Timeout(5.0))
        builder.set_reconnect_delay(ReconnectDelay(2.0))
        builder.set_reconnect_delay_max(ReconnectDelayMax(10.0))

    def test_default_initialization(self):
        builder = ModbusTCPClientBuilder()
        attributes = [
            builder.ip_address, builder.port, builder.coil_size,
            builder.discrete_input_size, builder.input_register_size,
            builder.holding_register_size, builder.timeout,
            builder.reconnect_delay, builder.reconnect_delay_max
        ]
        for attribute in attributes:
            self.assertIsNone(attribute)

    def test_build_with_missing_configuration(self):
        builder = ModbusTCPClientBuilder()

        # Missing IP address
        self.set_builder_with_required_fields(builder)
        builder._ip_address = None
        with self.assertRaises(AssertionError, msg="IP address must be set"):
            builder.build()

        # Missing Port
        builder = ModbusTCPClientBuilder()
        self.set_builder_with_required_fields(builder)
        builder._port = None
        with self.assertRaises(AssertionError, msg="Port must be set"):
            builder.build()

    def test_build_with_all_values_set(self):
        builder = ModbusTCPClientBuilder()
        self.set_builder_with_required_fields(builder)

        # Mock the client creation to ensure it is called with the builder
        with patch.object(MockModbusClient, '__init__', return_value=None) as mock_init:
            modbus_client = builder.build()
            mock_init.assert_called_once_with(builder)
            self.assertIsInstance(modbus_client, MockModbusClient)

    def test_set_ip_address(self):
        builder = ModbusTCPClientBuilder()
        ip = IPAddress('192.168.1.1')
        builder.set_ip_address(ip)
        self.assertEqual(builder.ip_address, ip)

    def test_set_port(self):
        builder = ModbusTCPClientBuilder()
        port = Port(502)
        builder.set_port(port)
        self.assertEqual(builder.port, port)

    def test_invalid_ip_address(self):
        builder = ModbusTCPClientBuilder()
        with self.assertRaises(AssertionError, msg="Invalid IP address format"):
            # noinspection PyTypeChecker
            builder.set_ip_address("invalid_ip")

    def test_invalid_port(self):
        builder = ModbusTCPClientBuilder()
        with self.assertRaises(AssertionError, msg="Invalid port value"):
            # noinspection PyTypeChecker
            builder.set_port(123456)

if __name__ == '__main__':
    unittest.main()