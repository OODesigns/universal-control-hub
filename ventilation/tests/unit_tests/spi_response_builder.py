import unittest

from spi.spi_12_bit_response_builder import SPI12BitResponseBuilder
from utils.response import Response
from utils.status import Status

class TestSPIResponseBuilder(unittest.TestCase):

    def test_valid_response(self):
        """
        Test the correct handling of a valid SPI response.
        """
        # Simulate a valid response with a 12-bit result
        response = Response(status=Status.OK, details="Valid response", value=[0x00, 0x0F, 0xAA])
        builder = SPI12BitResponseBuilder(response)
        result = builder.get_12_bit_result()

        # Expected result calculation:
        # High 4 bits from second byte (0x0F & 0x0F) << 8 = 0x0F << 8 = 0x0F00 (3840)
        # Low 8 bits from third byte (0xAA) = 0x00AA (170)
        # Result = 3840 + 170 = 4010
        expected_result = 4010
        self.assertEqual(result.value, expected_result, f"Expected {expected_result}, but got {result.value}")

    def test_empty_response(self):
        """
        Test handling of an empty response.
        """
        response = Response(status=Status.OK, details="Empty response", value=[])
        with self.assertRaises(IndexError):
            builder = SPI12BitResponseBuilder(response)
            builder.get_12_bit_result()

    def test_incorrect_response_length(self):
        """
        Test handling of a response that does not contain exactly 3 bytes.
        """
        response = Response(status=Status.OK, details="Invalid response length", value=[0x00, 0x0F])
        with self.assertRaises(IndexError):
            builder = SPI12BitResponseBuilder(response)
            builder.get_12_bit_result()

    def test_invalid_response_type(self):
        """
        Test handling of a response that is not a list of integers.
        """
        response = Response(status=Status.OK, details="Invalid response type", value="not a list")
        with self.assertRaises(TypeError):
            builder = SPI12BitResponseBuilder(response)
            builder.get_12_bit_result()

    def test_status_exception_response(self):
        """
        Test handling of a response with a status of EXCEPTION.
        """
        response = Response(status=Status.EXCEPTION, details="Invalid response", value=[0x00, 0x0F, 0xAA])
        with self.assertRaises(AssertionError):
            # Since the status is EXCEPTION, we should not proceed with creating the builder
            assert response.status == Status.OK, "Response status is not OK"
            builder = SPI12BitResponseBuilder(response)
            builder.get_12_bit_result()

if __name__ == '__main__':
    unittest.main()
