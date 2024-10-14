import unittest
from unittest.mock import MagicMock, patch

from adc.mcp3208 import MCP3208
from spi.spi import SPIInterface
from spi.spi_12_bit_response_builder import SPI12BitResponseBuilder
from utils.response import Response
from utils.status import Status
from spi.spi_values import SPIBusNumber, SPIChipSelect, SPIMaxSpeedHz, SPIMode, SPIBitsPerWord

class MockConfigLoader():
    def __init__(self, config):

        self.config = config

    def get_value(self, key):
        return self.config[key]

class TestMCP3208(unittest.TestCase):

    @classmethod
    def configure_mock_spi_client_builder(cls, mock_spi_client_builder):
        # Configure the mock to return itself for method chaining
        mock_spi_client_builder.return_value.set_bus.return_value = mock_spi_client_builder.return_value
        mock_spi_client_builder.return_value.set_chip_select.return_value = mock_spi_client_builder.return_value
        mock_spi_client_builder.return_value.set_max_speed_hz.return_value = mock_spi_client_builder.return_value
        mock_spi_client_builder.return_value.set_mode.return_value = mock_spi_client_builder.return_value
        mock_spi_client_builder.return_value.set_bits_per_word.return_value = mock_spi_client_builder.return_value

    @patch('adc.mcp3208.SPIClientBuilder')
    def test_mcp3208_initialization(self, mock_spi_client_builder):
        """
        Test the initialization of the MCP3208 class.
        """
        # Use helper method to configure the mock
        self.configure_mock_spi_client_builder(mock_spi_client_builder)

        mock_spi = MagicMock()
        mock_spi_client_builder.return_value.build.return_value = mock_spi

        config = {
            "spi_bus": 0,
            "spi_chip_select": 1,
        }
        config_loader = MockConfigLoader(config)

        # noinspection PyTypeChecker
        MCP3208(config_loader)

        # Assert that SPIClientBuilder was initialized with the right parameters
        mock_spi_client_builder.return_value.set_bus.assert_called_with(SPIBusNumber(0))
        mock_spi_client_builder.return_value.set_chip_select.assert_called_with(SPIChipSelect(1))
        mock_spi_client_builder.return_value.set_max_speed_hz.assert_called_with(SPIMaxSpeedHz(100000))
        mock_spi_client_builder.return_value.set_mode.assert_called_with(SPIMode(0))
        mock_spi_client_builder.return_value.set_bits_per_word.assert_called_with(SPIBitsPerWord(8))

        # Assert that build was called
        mock_spi_client_builder.return_value.build.assert_called_once()

    def test_spi_response_builder_valid(self):
        """
        Test the SPIResponseBuilder with a valid response.
        """
        response = Response(status=Status.OK, details="Valid response", value=[0x00, 0x0F, 0xAA])
        builder = SPI12BitResponseBuilder(response)
        result = builder.get_12_bit_result()

        # Expected result calculation:
        expected_result = ((0x0F & 0x0F) << 8) | 0xAA
        self.assertEqual(result, expected_result, f"Expected {expected_result}, but got {result}")

    def test_spi_response_builder_invalid_response_length(self):
        """
        Test the SPIResponseBuilder with an incorrect response length.
        """
        response = Response(status=Status.OK, details="Invalid response length", value=[0x00, 0x0F])
        with self.assertRaises(IndexError):
            builder = SPI12BitResponseBuilder(response)
            builder.get_12_bit_result()

    @patch('adc.mcp3208.SPIClientBuilder')
    def test_mcp3208_read_valid(self, mock_spi_client_builder):
        """
        Test the MCP3208 read method with a valid SPI response.
        """
        # Use helper method to configure the mock
        self.configure_mock_spi_client_builder(mock_spi_client_builder)

        # Mock the SPI instance returned by the builder
        mock_spi = MagicMock(spec=SPIInterface)  # Correctly spec the interface
        # Mock SPI execute response
        mock_spi.execute.return_value = Response(status=Status.OK, details="Valid response", value=[0x00, 0x0F, 0xAA])
        mock_spi_client_builder.return_value.build.return_value = mock_spi

        # Configuration for the MCP3208
        config = {
            "spi_bus": 0,
            "spi_chip_select": 1,
        }
        config_loader = MockConfigLoader(config)

        # Instantiate MCP3208 with mocked dependencies
        # noinspection PyTypeChecker
        device = MCP3208(config_loader)

        # Call the read method and verify the result
        result = device.read()
        expected_result = ((0x0F & 0x0F) << 8) | 0xAA
        self.assertEqual(result, expected_result, f"Expected {expected_result}, but got {result}")

    @patch('adc.mcp3208.SPIClientBuilder')
    def test_mcp3208_read_exception(self, mock_spi_client_builder):
        """
        Test the MCP3208 read method when the SPI client returns an exception response.
        """
        # Use helper method to configure the mock
        self.configure_mock_spi_client_builder(mock_spi_client_builder)

        mock_spi = MagicMock()
        # Mock SPI execute response with exception
        mock_spi.execute.return_value = Response(status=Status.EXCEPTION, details="SPI communication failed", value=[])
        mock_spi_client_builder.return_value.build.return_value = mock_spi

        config = {
            "spi_bus": 0,
            "spi_chip_select": 1,
        }
        config_loader = MockConfigLoader(config)
        # noinspection PyTypeChecker
        device = MCP3208(config_loader)

        # Expecting an exception to be raised due to invalid response status
        with self.assertRaises(IndexError):
            device.read()

if __name__ == '__main__':
    unittest.main()