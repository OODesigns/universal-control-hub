import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from pymodbus.client import ModbusBaseClient
from modbus.modbus_client_builder import ModbusClientBuilder
from py_modbus.modbus_connection_manager import ModbusConnectionManager
from py_modbus.modus_py_client import ModbusPYClient
from utils.operation_response import OperationStatus, OperationResponse

class TestModbusClient(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        # Mock the ModbusConnectionManager
        self.mock_client = AsyncMock(spec=ModbusBaseClient)
        self.mock_builder = MagicMock(spec=ModbusClientBuilder)
        self.mock_client_manager = MagicMock(spec=ModbusConnectionManager)

        # Patch ModbusClientManager to use our mock
        self.patcher = patch('py_modbus.modus_client.ModbusConnectionManager', return_value=self.mock_client_manager)
        self.patcher.start()

        # Create the ModbusClient instance
        self.modbus_client = ModbusPYClient(client=self.mock_client, builder=self.mock_builder)

    def tearDown(self):
        self.patcher.stop()

    async def test_connect_success(self):
        # Mock a successful connection response
        self.mock_client_manager.connect.return_value = OperationResponse(
            status=OperationStatus.OK,
            details="Connected successfully."
        )

        # Call the connect method
        response = await self.modbus_client.connect()

        # Assert the connect method was called and returned the expected response
        self.mock_client_manager.connect.assert_called_once()
        self.assertEqual(response.status, OperationStatus.OK)
        self.assertEqual(response.details, "Connected successfully.")

    async def test_connect_failure(self):
        # Mock a failed connection response
        self.mock_client_manager.connect.return_value = OperationResponse(
            status=OperationStatus.FAILED,
            details="Failed to connect to the server."
        )

        # Call the connect method
        response = await self.modbus_client.connect()

        # Assert the connect method was called and returned the expected response
        self.mock_client_manager.connect.assert_called_once()
        self.assertEqual(response.status, OperationStatus.FAILED)
        self.assertEqual(response.details, "Failed to connect to the server.")

    def test_disconnect_success(self):
        # Mock a successful disconnection response
        self.mock_client_manager.disconnect.return_value = OperationResponse(
            status=OperationStatus.OK,
            details="Disconnected successfully."
        )

        # Call the disconnect method
        response = self.modbus_client.disconnect()

        # Assert the disconnect method was called and returned the expected response
        self.mock_client_manager.disconnect.assert_called_once()
        self.assertEqual(response.status, OperationStatus.OK)
        self.assertEqual(response.details, "Disconnected successfully.")

    def test_disconnect_failure(self):
        # Mock a failed disconnection response
        self.mock_client_manager.disconnect.return_value = OperationResponse(
            status=OperationStatus.FAILED,
            details="Client was not connected or was already closed."
        )

        # Call the disconnect method
        response = self.modbus_client.disconnect()

        # Assert the disconnect method was called and returned the expected response
        self.mock_client_manager.disconnect.assert_called_once()
        self.assertEqual(response.status, OperationStatus.FAILED)
        self.assertEqual(response.details, "Client was not connected or was already closed.")

    async def test_read_success(self):
        # Mock results for the readers
        mock_coils_result = AsyncMock()
        mock_discrete_result = AsyncMock()
        mock_input_result = AsyncMock()
        mock_holding_result = AsyncMock()

        self.modbus_client._coils_reader.read = AsyncMock(return_value=mock_coils_result)
        self.modbus_client._discrete_inputs.read = AsyncMock(return_value=mock_discrete_result)
        self.modbus_client._input_registers.read = AsyncMock(return_value=mock_input_result)
        self.modbus_client._holding_registers.read = AsyncMock(return_value=mock_holding_result)

        # Call the read method
        result = await self.modbus_client.read()

        # Assert that read methods were called and returned expected results
        self.modbus_client._coils_reader.read.assert_called_once_with(0, self.modbus_client.coil_size.value)
        self.modbus_client._discrete_inputs.read.assert_called_once_with(0, self.modbus_client.discrete_input_size.value)
        self.modbus_client._input_registers.read.assert_called_once_with(0, self.modbus_client.input_register_size.value)
        self.modbus_client._holding_registers.read.assert_called_once_with(0, self.modbus_client.holding_register_size.value)

        # Assert the result contains the mocked data
        self.assertEqual(result.coils, mock_coils_result)
        self.assertEqual(result.discrete_inputs, mock_discrete_result)
        self.assertEqual(result.input_register, mock_input_result)
        self.assertEqual(result.holding_register, mock_holding_result)


if __name__ == '__main__':
    unittest.main()
