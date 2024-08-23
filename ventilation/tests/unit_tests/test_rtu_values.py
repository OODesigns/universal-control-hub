import unittest
from unittest.mock import patch
from utils.rtu_values import BaudRate, StopBits, SerialPort


class TestRTUValues(unittest.TestCase):

    # BaudRate Tests
    def test_baud_rate_valid(self):
        valid_baud_rates = [9600, 14400, 19200, 38400, 57600, 115200]
        for rate in valid_baud_rates:
            with self.subTest(rate=rate):
                self.assertEqual(BaudRate(rate).value, rate)

    def test_baud_rate_invalid(self):
        invalid_baud_rates = [12345, 2400, 4800, 256000]
        for rate in invalid_baud_rates:
            with self.subTest(rate=rate):
                with self.assertRaises(ValueError):
                    BaudRate(rate)

    # StopBits Tests
    def test_stop_bits_valid(self):
        valid_stop_bits = [1, 1.5, 2]
        for bits in valid_stop_bits:
            with self.subTest(bits=bits):
                self.assertEqual(StopBits(bits).value, bits)

    def test_stop_bits_invalid(self):
        invalid_stop_bits = [0, 3, 2.5, -1]
        for bits in invalid_stop_bits:
            with self.subTest(bits=bits):
                with self.assertRaises(ValueError):
                    StopBits(bits)

    # Windows Tests
    def test_serial_port_valid_windows(self):
        valid_ports = ["COM1", "COM2", "COM10", "COM123"]
        with patch('platform.system', return_value='Windows'):
            for port in valid_ports:
                with self.subTest(port=port):
                    self.assertEqual(SerialPort(port).value, port)

    def test_serial_port_invalid_windows(self):
        invalid_ports = ["COM0", "COM", "COMA", "COM1A", "/dev/ttyS0"]
        with patch('platform.system', return_value='Windows'):
            for port in invalid_ports:
                with self.subTest(port=port):
                    with self.assertRaises(ValueError):
                        SerialPort(port)

    # Linux Tests
    @patch('platform.system', return_value='Linux')
    def test_serial_port_valid_linux(self, mock_platform):
        valid_ports = ["/dev/ttyS0", "/dev/ttyUSB0", "/dev/ttyS1", "/dev/ttyUSB1", "/dev/ttyS10", "/dev/ttyUSB99"]
        for port in valid_ports:
            with self.subTest(port=port):
                self.assertEqual(SerialPort(port).value, port)

    def test_serial_port_invalid_linux(self):
        invalid_ports = [
            "COM1",
            "ttyS0",
            "/dev/ttyS",
            "/dev/ttyUSB",
            "/dev/ttyUSB01",
            "/dev/ttyS001",
            "/dev/ttyUSB-1",
            "/dev/ttyUSBa",
            "/dev/ttyUSB ",
            "/dev/ttyUSB1a"
        ]
        with patch('platform.system', return_value='Linux'):
            for port in invalid_ports:
                with self.subTest(port=port):
                    with self.assertRaises(ValueError):
                        SerialPort(port)


    def test_serial_port_valid_darwin(self):
        valid_ports = ["/dev/ttyS0", "/dev/ttyUSB0", "/dev/ttyS2", "/dev/ttyUSB3"]
        with patch('platform.system', return_value='Darwin'):
            for port in valid_ports:
                with self.subTest(port=port):
                    self.assertEqual(SerialPort(port).value, port)

    def test_serial_port_invalid_darwin(self):
        invalid_ports = ["COM1", "ttyUSB0", "/dev/tty", "/dev/ttyUSB_", "/dev/ttyS-1"]
        with patch('platform.system', return_value='Darwin'):
            for port in invalid_ports:
                with self.subTest(port=port):
                    with self.assertRaises(ValueError):
                        SerialPort(port)

if __name__ == '__main__':
    unittest.main()
