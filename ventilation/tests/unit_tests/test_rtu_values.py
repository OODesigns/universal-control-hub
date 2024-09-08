import unittest
import platform

from modbus.rtu_values import SerialPort, StrictSerialPort, BaudRate, StrictBaudRate, StopBits, StrictStopBits
from utils.status import Status


class TestRTUValues(unittest.TestCase):

    # Test for SerialPort class (non-strict)
    def test_serial_port_valid(self):
        system = platform.system()
        if system == "Windows":
            valid_ports = ["COM1", "COM2", "COM10", "COM100"]
        elif system in ["Linux", "Darwin"]:
            valid_ports = ["/dev/ttyS0", "/dev/ttyUSB0", "/dev/ttyUSB1", "/dev/ttyS10"]
        else:
            valid_ports = []

        for port in valid_ports:
            with self.subTest(port=port):
                serial_port = SerialPort(port)
                self.assertEqual(serial_port.status, Status.OK)
                self.assertEqual(serial_port.value, port)
                self.assertEqual(serial_port.details, "Validation successful")

    def test_serial_port_invalid(self):
        system = platform.system()
        if system == "Windows":
            invalid_ports = ["COM", "COM0", "COMABC"]
        elif system in ["Linux", "Darwin"]:
            invalid_ports = ["/dev/ttyX0", "/dev/ttyUSBa", "/dev/serial0"]
        else:
            invalid_ports = ["InvalidPort"]

        for port in invalid_ports:
            with self.subTest(port=port):
                serial_port = SerialPort(port)
                self.assertEqual(serial_port.status, Status.EXCEPTION)
                self.assertIsNone(serial_port.value)
                self.assertIn("Invalid serial port", serial_port.details)

    # Test for StrictSerialPort class (strict)
    def test_strict_serial_port_invalid(self):
        invalid_ports = ["COM0", "/dev/ttyUSBa", "InvalidPort"]
        for port in invalid_ports:
            with self.subTest(port=port):
                with self.assertRaises(ValueError):
                    StrictSerialPort(port)

    # Test for BaudRate class (non-strict)
    def test_baud_rate_valid(self):
        valid_baud_rates = [9600, 14400, 19200, 38400, 57600, 115200]
        for rate in valid_baud_rates:
            with self.subTest(rate=rate):
                baud_rate = BaudRate(rate)
                self.assertEqual(baud_rate.status, Status.OK)
                self.assertEqual(baud_rate.value, rate)
                self.assertEqual(baud_rate.details, "Validation successful")

    def test_baud_rate_invalid(self):
        invalid_baud_rates = [12345, 15000, "9600", -9600]
        for rate in invalid_baud_rates:
            with self.subTest(rate=rate):
                baud_rate = BaudRate(rate)
                self.assertEqual(baud_rate.status, Status.EXCEPTION)
                self.assertIsNone(baud_rate.value)

    # Test for StrictBaudRate class (strict)
    def test_strict_baud_rate_invalid(self):
        invalid_baud_rates = [12345, 15000, "9600", -9600]
        for rate in invalid_baud_rates:
            with self.subTest(rate=rate):
                with self.assertRaises(ValueError):
                    StrictBaudRate(rate)

    # Test for StopBits class (non-strict)
    def test_stop_bits_valid(self):
        valid_stop_bits = [1, 2]
        for bits in valid_stop_bits:
            with self.subTest(bits=bits):
                stop_bits = StopBits(bits)
                self.assertEqual(stop_bits.status, Status.OK)
                self.assertEqual(stop_bits.value, bits)
                self.assertEqual(stop_bits.details, "Validation successful")

    def test_stop_bits_invalid(self):
        invalid_stop_bits = [0, 1.5, 3, "2"]
        for bits in invalid_stop_bits:
            with self.subTest(bits=bits):
                stop_bits = StopBits(bits)
                self.assertEqual(stop_bits.status, Status.EXCEPTION)
                self.assertIsNone(stop_bits.value)

    # Test for StrictStopBits class (strict)
    def test_strict_stop_bits_invalid(self):
        invalid_stop_bits = [0, 1.5, 3, "2"]
        for bits in invalid_stop_bits:
            with self.subTest(bits=bits):
                with self.assertRaises(ValueError):
                    StrictStopBits(bits)


if __name__ == '__main__':
    unittest.main()
