import unittest

from utils.tcp_values import IPAddress, Port, Timeout


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
                self.assertEqual(IPAddress(ip).value, ip)

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
                with self.assertRaises(ValueError):
                    IPAddress(ip)

    # Test for Port class
    def test_port_valid(self):
        port = Port(502)
        self.assertEqual(port.value, 502)
        port = Port(0)
        self.assertEqual(port.value, 0)
        port = Port(65535)
        self.assertEqual(port.value, 65535)

    def test_port_invalid(self):
        with self.assertRaises(ValueError):
            Port(-1)
        with self.assertRaises(ValueError):
            Port(70000)

    # Test for Timeout class
    def test_timeout_valid(self):
        timeout = Timeout(30)
        self.assertEqual(timeout.value, 30)
        timeout = Timeout(0)
        self.assertEqual(timeout.value, 0)
        timeout = Timeout(60)
        self.assertEqual(timeout.value, 60)

    def test_timeout_invalid(self):
        with self.assertRaises(ValueError):
            Timeout(-1)
        with self.assertRaises(ValueError):
            Timeout(61)

if __name__ == '__main__':
    unittest.main()
