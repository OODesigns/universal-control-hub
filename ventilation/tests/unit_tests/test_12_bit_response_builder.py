import unittest
from unittest.mock import MagicMock

from spi.spi_12_bit_response_builder import SPI12BitResponseBuilder
from utils.response import Response


class TestSPI12BitResponseBuilder(unittest.TestCase):

    def setUp(self):
        # Example response: 3 bytes representing the SPI response
        self.response_mock = MagicMock(spec=Response)
        self.response_mock.value = [0x00, 0x3F, 0xA5]  # Example byte values
        self.builder = SPI12BitResponseBuilder(self.response_mock)

    def test_extract_high_bits(self):
        # Extract high 4 bits from the second byte (0x3F)
        expected_high_bits = (0x3F & 0x0F) << 8  # Should be 0x0F << 8 = 0x0F00
        self.assertEqual(self.builder.extract_high_bits(), expected_high_bits)

    def test_extract_low_bits(self):
        # Extract low 8 bits from the third byte (0xA5)
        expected_low_bits = 0xA5
        self.assertEqual(self.builder.extract_low_bits(), expected_low_bits)

    def test_get_12_bit_result(self):
        # Combine high bits and low bits to form a 12-bit result
        expected_result = ((0x3F & 0x0F) << 8) | 0xA5  # Should be 0x0FA5
        self.assertEqual(self.builder.get_12_bit_result(), expected_result)


if __name__ == '__main__':
    unittest.main()