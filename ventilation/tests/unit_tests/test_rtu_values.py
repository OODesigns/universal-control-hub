import unittest
from unittest.mock import patch
from utils.rtu_values import BaudRate, StopBits, SerialPort, StrictBaudRate, StrictStopBits, StrictSerialPort
from utils.value import ValueStatus


class TestRTUValues(unittest.TestCase):

    # BaudRate Tests
    def test_baud_rate_valid(self):
        valid_baud_rates = [9600, 14400, 19200, 38400, 57600, 115200]
        for rate in valid_baud_rates:
            with self.subTest(rate=rate):
                baud_rate = BaudRate(rate)
                self.assertEqual(baud_rate.value, rate)
                self.assertEqual(baud_rate.status, ValueStatus.OK)
                self.assertEqual(baud_rate.details, "")

    def test_baud_rate_invalid(self):
        invalid_baud_rates = [12345, 2400, 4800, 256000]
        for rate in invalid_baud_rates:
            with self.subTest(rate=rate):
                baud_rate = BaudRate(rate)
                self.assertEqual(baud_rate.status, ValueStatus.EXCEPTION)
                self.assertTrue("Invalid baud rate" in baud_rate.details)
                with self.assertRaises(ValueError):
                    _ = baud_rate.value

    def test_strict_baud_rate_invalid(self):
        invalid_baud_rates = [12345, 2400, 4800, 256000]
        for rate in invalid_baud_rates:
            with self.subTest(rate=rate):
                with self.assertRaises(ValueError):
                    StrictBaudRate(rate)

    # StopBits Tests
    def test_stop_bits_valid(self):
        valid_stop_bits = [1, 1.5, 2]
        for bits in valid_stop_bits:
            with self.subTest(bits=bits):
                stop_bits = StopBits(bits)
                self.assertEqual(stop_bits.value, bits)
                self.assertEqual(stop_bits.status, ValueStatus.OK)
                self.assertEqual(stop_bits.details, "")

    def test_stop_bits_invalid(self):
        invalid_stop_bits = [0, 3, 2.5, -1]
        for bits in invalid_stop_bits:
            with self.subTest(bits=bits):
                stop_bits = StopBits(bits)
                self.assertEqual(stop_bits.status, ValueStatus.EXCEPTION)
                self.assertTrue("Invalid stop bits" in stop_bits.details)
                with self.assertRaises(ValueError):
                    _ = stop_bits.value

    def test_strict_stop_bits_invalid(self):
        invalid_stop_bits = [0, 3, 2.5, -1]
        for bits in invalid_stop_bits:
            with self.subTest(bits=bits):
                with self.assertRaises(ValueError):
                    StrictStopBits(bits)

    # Windows Tests for SerialPort
    def test_serial_port_valid_windows(self):
        valid_ports = ["COM1", "COM2", "COM10", "COM123"]
        with patch('platform.system', return_value='Windows'):
            for port in valid_ports:
                with self.subTest(port=port):
                    serial_port = SerialPort(port)
                    self.assertEqual(serial_port.value, port)
                    self.assertEqual(serial_port.status, ValueStatus.OK)
                    self.assertEqual(serial_port.details, "")

    def test_serial_port_invalid_windows(self):
        invalid_ports = ["COM0", "COM", "COMA", "COM1A", "/dev/ttyS0"]
        with patch('platform.system', return_value='Windows'):
            for port in invalid_ports:
                with self.subTest(port=port):
                    serial_port = SerialPort(port)
                    self.assertEqual(serial_port.status, ValueStatus.EXCEPTION)
                    self.assertTrue("Invalid serial port" in serial_port.details)
                    with self.assertRaises(ValueError):
                        _ = serial_port.value

    def test_strict_serial_port_invalid_windows(self):
        invalid_ports = ["COM0", "COM", "COMA", "COM1A", "/dev/ttyS0"]
        with patch('platform.system', return_value='Windows'):
            for port in invalid_ports:
                with self.subTest(port=port):
                    with self.assertRaises(ValueError):
                        StrictSerialPort(port)

    # Linux Tests for SerialPort
    def test_serial_port_valid_linux(self):
        valid_ports = ["/dev/ttyS0", "/dev/ttyUSB0", "/dev/ttyS1", "/dev/ttyUSB1", "/dev/ttyS10", "/dev/ttyUSB99"]
        with patch('platform.system', return_value='Linux'):
            for port in valid_ports:
                with self.subTest(port=port):
                    serial_port = SerialPort(port)
                    self.assertEqual(serial_port.value, port)
                    self.assertEqual(serial_port.status, ValueStatus.OK)
                    self.assertEqual(serial_port.details, "")

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
                    serial_port = SerialPort(port)
                    self.assertEqual(serial_port.status, ValueStatus.EXCEPTION)
                    self.assertTrue("Invalid serial port" in serial_port.details)
                    with self.assertRaises(ValueError):
                        _ = serial_port.value

    def test_strict_serial_port_invalid_linux(self):
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
                        StrictSerialPort(port)

    # Darwin Tests for SerialPort
    def test_serial_port_valid_darwin(self):
        valid_ports = ["/dev/ttyS0", "/dev/ttyUSB0", "/dev/ttyS2", "/dev/ttyUSB3"]
        with patch('platform.system', return_value='Darwin'):
            for port in valid_ports:
                with self.subTest(port=port):
                    serial_port = SerialPort(port)
                    self.assertEqual(serial_port.value, port)
                    self.assertEqual(serial_port.status, ValueStatus.OK)
                    self.assertEqual(serial_port.details, "")

    def test_serial_port_invalid_darwin(self):
        invalid_ports = ["COM1", "ttyUSB0", "/dev/tty", "/dev/ttyUSB_", "/dev/ttyS-1"]
        with patch('platform.system', return_value='Darwin'):
            for port in invalid_ports:
                with self.subTest(port=port):
                    serial_port = SerialPort(port)
                    self.assertEqual(serial_port.status, ValueStatus.EXCEPTION)
                    self.assertTrue("Invalid serial port" in serial_port.details)
                    with self.assertRaises(ValueError):
                        _ = serial_port.value

    def test_strict_serial_port_invalid_darwin(self):
        invalid_ports = ["COM1", "ttyUSB0", "/dev/tty", "/dev/ttyUSB_", "/dev/ttyS-1"]
        with patch('platform.system', return_value='Darwin'):
            for port in invalid_ports:
                with self.subTest(port=port):
                    with self.assertRaises(ValueError):
                        StrictSerialPort(port)


if __name__ == '__main__':
    unittest.main()
