import unittest
from unittest.mock import AsyncMock, MagicMock
from blauberg.blauberg_mvhr import BlaubergMVHR
from blauberg.blauberg_mvhr_state import BlaubergMVHRState
from modbus.modbus import ModbusData
from modbus.modbus_tcp_client_builder import ModbusTCPClientBuilder
from utils.operation_response import OperationResponse, OperationStatus
from utils.response import Response
from utils.status import Status


class TestBlaubergMVHR(unittest.IsolatedAsyncioTestCase):

    @classmethod
    def setUpClass(cls):
        # Register the mock Modbus TCP client
        ModbusTCPClientBuilder.register_client(client_class=AsyncMock)

    def setUp(self):
        # Mock configuration loader and modbus factory
        self.mock_config_loader = MagicMock()
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

        # Initialize the BlaubergMVHR object
        self.blauberg_mvhr = BlaubergMVHR(self.mock_config_loader)
        self.blauberg_mvhr._modbus = self.mock_modbus_interface  # Inject the mock modbus interface

    async def test_read_data(self):
        """Test that read_data returns a BlaubergMVHRState instance based on the Modbus read."""
        # Mock the input_register values for valid temperatures
        mock_modbus_data = MagicMock(spec=ModbusData)

        # Set the input_register response to the mock
        mock_modbus_data.input_register = Response(
            status=Status.OK,
            details="Valid input register data",
            value=[0, 250, 300]
        )

        # Mock the Modbus read to return valid input register data
        self.mock_modbus_interface.read.return_value = mock_modbus_data

        # Call the read_data method
        result = await self.blauberg_mvhr.read()

        # Ensure the Modbus read method was called
        self.mock_modbus_interface.read.assert_called_once()

        # Verify that the result is an instance of BlaubergMVHRState
        self.assertIsInstance(result, BlaubergMVHRState)
        self.assertEqual(result.temp_supply_in.value, 25.0)  # 250 converted to 25.0°C
        self.assertEqual(result.temp_supply_out.value, 30.0)  # 300 converted to 30.0°C

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

    # noinspection PyUnresolvedReferences
    async def test_stop(self):
        """Test that the stop method disconnects from the Modbus interface and returns a success response."""
        # Mock the Modbus interface disconnect method to return a successful response
        self.mock_modbus_interface.disconnect.return_value = OperationResponse(status=OperationStatus.OK, details="Disconnected")

        # Call the stop method, should not have await but the test is an async mock
        response = await self.blauberg_mvhr.close()

        # Ensure the Modbus disconnect method was called
        self.mock_modbus_interface.disconnect.assert_called_once()

        # Verify the response is correct
        self.assertEqual(response.status, OperationStatus.OK)
        self.assertEqual(response.details, "Disconnected")

        # Await the mock disconnect coroutine to prevent RuntimeWarning
        if hasattr(self.mock_modbus_interface.disconnect, "awaited"):
            self.mock_modbus_interface.disconnect.awaited = True


if __name__ == '__main__':
    unittest.main()