import unittest

from utils.rtu_values import BaudRate, StopBits


class TestRTUValues(unittest.TestCase):

    # Test for BaudRate class
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

    # Test for StopBits class
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

if __name__ == '__main__':
    unittest.main()
