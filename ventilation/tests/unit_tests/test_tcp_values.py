import unittest
from modbus.tcp_values import IPAddress, Port, StrictIPAddress, StrictPort
from utils.value import ValueStatus

class TestTCPValues(unittest.TestCase):

    # Test for IPAddress class
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
                self.assertEqual(ip_address.status, ValueStatus.OK)
                self.assertEqual(ip_address.details, "")

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
                self.assertEqual(ip_address.status, ValueStatus.EXCEPTION)
                self.assertTrue("Invalid IP address" in ip_address.details)
                with self.assertRaises(ValueError):
                    _ = ip_address.value  # Accessing the value should raise ValueError

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
                with self.assertRaises(ValueError):
                    StrictIPAddress(ip)

class TestPort(unittest.TestCase):

    def test_port_valid(self):
        valid_ports = [0, 80, 8080, 65535]
        for port_num in valid_ports:
            with self.subTest(port=port_num):
                port = Port(port_num)
                self.assertEqual(port.value, port_num)
                self.assertEqual(port.status, ValueStatus.OK)

    def test_port_invalid(self):
        invalid_ports = [-1, 70000, "8080", 65536]
        for port_num in invalid_ports:
            with self.subTest(port=port_num):
                port = Port(port_num)
                self.assertEqual(port.status, ValueStatus.EXCEPTION)
                with self.assertRaises(ValueError):
                    _ = port.value

    def test_strict_port_invalid(self):
        invalid_ports = [-1, 70000, "8080", 65536]
        for port_num in invalid_ports:
            with self.subTest(port=port_num):
                with self.assertRaises(ValueError):
                    StrictPort(port_num)

if __name__ == '__main__':
    unittest.main()
