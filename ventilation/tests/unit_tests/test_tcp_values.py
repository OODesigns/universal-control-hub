import unittest
from modbus.tcp_values import IPAddress, Port, StrictIPAddress, StrictPort
from utils.status import Status

class TestTCPValues(unittest.TestCase):

    # Test for IPAddress class (non-strict)
    def test_ip_address_valid(self):
        valid_ips = [
            "0.0.0.0",
            "127.0.0.1",
            "192.168.1.1",
            "255.255.255.255",
            "10.0.0.1",
            "172.16.0.1"
        ]
        for ip in valid_ips:
            with self.subTest(ip=ip):
                ip_address = IPAddress(ip)
                self.assertEqual(ip_address.value, ip)
                self.assertEqual(ip_address.status, Status.OK)
                self.assertEqual(ip_address.details, "validation successful")

    def test_ip_address_invalid(self):
        invalid_ips = [
            "999.999.999.999",
            "256.256.256.256",
            "192.168.1.256",
            "192.168.1.-1",
            "192.168.1",
            "192.168.1.1.1",
            "abc.def.ghi.jkl",
            "192.168.01.1",  # Invalid due to leading zero
            "192.168.1.1. ",
            "192.168.1.1.",
            "1234.123.123.123"
        ]
        for ip in invalid_ips:
            with self.subTest(ip=ip):
                ip_address = IPAddress(ip)
                self.assertEqual(ip_address.status, Status.EXCEPTION)
                self.assertIn("Invalid IP address", ip_address.details)
                self.assertIsNone(ip_address.value)

    # Test for StrictIPAddress class (strict)
    def test_strict_ip_address_invalid(self):
        invalid_ips = [
            "999.999.999.999",
            "256.256.256.256",
            "192.168.1.256",
            "192.168.1.-1",
            "192.168.1",
            "192.168.1.1.1",
            "abc.def.ghi.jkl",
            "192.168.01.1",
            "192.168.1.1. ",
            "192.168.1.1.",
            "1234.123.123.123"
        ]
        for ip in invalid_ips:
            with self.subTest(ip=ip):
                # Expecting strict validation to raise ValueError
                with self.assertRaises(ValueError):
                    StrictIPAddress(ip)

class TestPort(unittest.TestCase):

    # Test for Port class (non-strict)
    def test_port_valid(self):
        valid_ports = [0, 80, 8080, 65535]
        for port_num in valid_ports:
            with self.subTest(port=port_num):
                port = Port(port_num)
                self.assertEqual(port.value, port_num)
                self.assertEqual(port.status, Status.OK)
                self.assertEqual(port.details, "validation successful")

    def test_port_invalid(self):
        invalid_ports = [-1, 70000, "8080", 65536]
        for port_num in invalid_ports:
            with self.subTest(port=port_num):
                port = Port(port_num)
                self.assertEqual(port.status, Status.EXCEPTION)
                self.assertIsNone(port.value)

    # Test for StrictPort class (strict)
    def test_strict_port_invalid(self):
        invalid_ports = [-1, 70000, "8080", 65536]
        for port_num in invalid_ports:
            with self.subTest(port=port_num):
                # Expecting strict validation to raise ValueError
                with self.assertRaises(ValueError):
                    StrictPort(port_num)

if __name__ == '__main__':
    unittest.main()
