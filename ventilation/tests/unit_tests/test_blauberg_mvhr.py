import unittest
from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch
from blauberg.blauberg_mvhr import BlaubergMVHR
from blauberg.blauberg_mvhr_state import BlaubergMVHRState
from utils.operation_response import OperationResponse, OperationStatus


class TestBlaubergMVHR(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        # Mock configuration loader and modbus factory
        self.mock_config_loader = MagicMock()
        self.mock_modbus_factory = MagicMock()
        self.mock_modbus_interface = AsyncMock()

        # Set up the config loader to return valid numeric values, including reconnect delay and max delay
        self.mock_config_loader.get_value.side_effect = lambda key: {
            "mvhr-timeout": 10.0,  # Timeout for Modbus communication
            "mvhr-port": 502,  # Example for the port
            "mvhr-ip-address": "192.168.0.100",  # Example for IP address
            "mvhr-retries": 3,  # Example for retries
            "mvhr-reconnect-delay": 0.1,  # Reconnect delay
            "mvhr-reconnect-delay-max": 300.0,  # Max reconnect delay
        }[key]

        # Set up the Modbus factory to return the mocked Modbus interface
        self.mock_modbus_factory.create_modbus.return_value = self.mock_modbus_interface

        # Initialize the BlaubergMVHR object
        self.blauberg_mvhr = BlaubergMVHR(self.mock_config_loader)

    async def test_read_data(self):
        """Test that read_data returns a BlaubergMVHRState instance based on the Modbus read."""
        # Call the read_data method
        with patch("blauberg.blauberg_mvhr_state.BlaubergTemperature") as mock_temperature_class :
            # Create a mock instance of BlaubergTemperature
            mock_temperature_instance = mock_temperature_class.return_value
            # Mock the value property to return 123
            type(mock_temperature_instance).value = PropertyMock(return_value=123)

            result = await self.blauberg_mvhr.read()

            # Ensure the Modbus read method was called
            self.mock_modbus_interface.read.assert_called_once()

            # Verify that the result is an instance of BlaubergMVHRState
            self.assertIsInstance(result, BlaubergMVHRState)
            self.assertEqual(result.temp_supply_in.value, 123)  # 250 converted to Celsius
            self.assertEqual(result.temp_supply_out.value, 123)  # 250 converted to Celsius


    async def test_start(self):
        """Test that the start method connects to the Modbus interface and returns a success response."""
        # Mock the Modbus interface connect method to return a successful response
        self.mock_modbus_interface.connect.return_value = OperationResponse(status=OperationStatus.OK, details="Connected")

        # Call the start method
        response = await self.blauberg_mvhr.open()

        # Ensure the Modbus connect method was called
        self.mock_modbus_interface.connect.assert_called_once()

        # Verify the response is correct
        self.assertEqual(response.status, OperationStatus.OK)
        self.assertEqual(response.details, "Connected")

    async def test_stop(self):
        """Test that the stop method disconnects from the Modbus interface and returns a success response."""
        # Mock the Modbus interface disconnect method to return a successful response
        self.mock_modbus_interface.disconnect.return_value = OperationResponse(status=OperationStatus.OK, details="Disconnected")

        # Call the stop method this method is NOT async, but we are using async mock so needed to add await
        # even though normally you would not use it

        # noinspection PyUnresolvedReferences
        response = await self.blauberg_mvhr.close()

        # Ensure the Modbus disconnect method was called
        self.mock_modbus_interface.disconnect.assert_called_once()

        # Verify the response is correct
        self.assertEqual(response.status, OperationStatus.OK)
        self.assertEqual(response.details, "Disconnected")


if __name__ == '__main__':
    unittest.main()
