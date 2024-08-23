import unittest

from devices.modbus_tcp_builder import ModbusTCPBuilder
from utils.tcp_values import IPAddress, Port
from devices.modbus_tcp import ModbusTCP

class TestModbusTCPBuilder(unittest.TestCase):

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

    def test_build_valid(self):
        builder = ModbusTCPBuilder()
        builder.set_ip_address(IPAddress('192.168.1.1')).set_port(Port(502))
        modbus_tcp = builder.build()
        self.assertIsInstance(modbus_tcp, ModbusTCP)

    def test_build_without_ip_address(self):
        builder = ModbusTCPBuilder()
        builder.set_port(Port(502))
        with self.assertRaises(ValueError):
            builder.build()

    def test_build_without_port(self):
        builder = ModbusTCPBuilder()
        builder.set_ip_address(IPAddress('192.168.1.1'))
        with self.assertRaises(ValueError):
            builder.build()

    def test_invalid_ip_address(self):
        builder = ModbusTCPBuilder()
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            builder.set_ip_address("invalid_ip")

    def test_invalid_port(self):
        builder = ModbusTCPBuilder()
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            builder.set_port(123456)  # Assuming Port validation restricts this range

if __name__ == '__main__':
    unittest.main()
