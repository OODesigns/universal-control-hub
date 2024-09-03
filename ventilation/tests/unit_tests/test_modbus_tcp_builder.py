import unittest
from unittest.mock import patch, MagicMock

from modbus.modbus_tcp_builder import ModbusTCPBuilder
from modbus.tcp_values import IPAddress, Port
from modbus.modbus import ModbusInterface

# Mock subclass of ModbusInterface for testing purposes
class MockModbusInterface(ModbusInterface):
    def connect(self):
        pass

    def disconnect(self):
        pass

    def read(self):
        pass

class TestModbusTCPBuilder(unittest.TestCase):

    def test_set_ip_address(self):
        builder = ModbusTCPBuilder(client_class=MockModbusInterface)
        ip = IPAddress('192.168.1.1')
        builder.set_ip_address(ip)
        self.assertEqual(builder.ip_address, ip)

    def test_set_port(self):
        builder = ModbusTCPBuilder(client_class=MockModbusInterface)
        port = Port(502)
        builder.set_port(port)
        self.assertEqual(builder.port, port)

    def test_build_valid(self):
        builder = ModbusTCPBuilder(client_class=MockModbusInterface)
        builder.set_ip_address(IPAddress('192.168.1.1')).set_port(Port(502))

        with patch.object(MockModbusInterface, '__init__', return_value=None) as mock_init:
            modbus_tcp = builder.build()
            mock_init.assert_called_once_with(builder)
            self.assertIsInstance(modbus_tcp, MockModbusInterface)

    def test_build_without_ip_address(self):
        builder = ModbusTCPBuilder(client_class=MockModbusInterface)
        builder.set_port(Port(502))
        with self.assertRaises(AssertionError):  # Changed to AssertionError
            builder.build()

    def test_build_without_port(self):
        builder = ModbusTCPBuilder(client_class=MockModbusInterface)
        builder.set_ip_address(IPAddress('192.168.1.1'))
        with self.assertRaises(AssertionError):  # Changed to AssertionError
            builder.build()

    def test_invalid_ip_address(self):
        builder = ModbusTCPBuilder(client_class=MockModbusInterface)
        with self.assertRaises(AssertionError):  # Changed to AssertionError
            # noinspection PyTypeChecker
            builder.set_ip_address("invalid_ip")

    def test_invalid_port(self):
        builder = ModbusTCPBuilder(client_class=MockModbusInterface)
        with self.assertRaises(AssertionError):  # Changed to AssertionError
            # noinspection PyTypeChecker
            builder.set_port(123456)  # Assuming Port validation restricts this range

if __name__ == '__main__':
    unittest.main()
