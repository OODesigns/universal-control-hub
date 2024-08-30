import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from pymodbus.client import ModbusBaseClient

from modbus.pymodbus.modbus_client_manager import ModbusClientManager, ConnectionResponse, ConnectionStatus
from modbus.pymodbus.modus_base import ModbusBase
from modbus.pymodbus.py_modbus_result import PyModbusCoilResult, PyModbusDiscreteInputResult, PyModbusInputRegisterResult, PyModbusHoldingRegisterResult
from modbus.modbus_builder import ModbusBuilder
from modbus.modbus_reader import ModbusBitReader, ModbusWordReader
from modbus.modbus import ModbusData

class TestModbusBase(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        # Mock the ModbusClientManager
        self.mock_client = AsyncMock(spec=ModbusBaseClient)
        self.mock_builder = MagicMock(spec=ModbusBuilder)
        self.mock_client_manager = MagicMock(spec=ModbusClientManager)

        # Patch ModbusClientManager to use our mock
        self.patcher = patch('modbus.pymodbus.modus_base.ModbusClientManager', return_value=self.mock_client_manager)
        self.patcher.start()

        # Create the ModbusBase instance
        self.modbus_base = ModbusBase(client=self.mock_client, builder=self.mock_builder)

    def tearDown(self):
        self.patcher.stop()

    async def test_connect_success(self):
        # Mock a successful connection response
        self.mock_client_manager.connect.return_value = ConnectionResponse(
            status=ConnectionStatus.OK,
            details="Connected successfully."
        )

        # Call the connect method
        response = await self.modbus_base.connect()

        # Assert the connect method was called and returned the expected response
        self.mock_client_manager.connect.assert_called_once()
        self.assertEqual(response.status, ConnectionStatus.OK)
        self.assertEqual(response.details, "Connected successfully.")

    async def test_connect_failure(self):
        # Mock a failed connection response
        self.mock_client_manager.connect.return_value = ConnectionResponse(
            status=ConnectionStatus.FAILED,
            details="Failed to connect to the server."
        )

        # Call the connect method
        response = await self.modbus_base.connect()

        # Assert the connect method was called and returned the expected response
        self.mock_client_manager.connect.assert_called_once()
        self.assertEqual(response.status, ConnectionStatus.FAILED)
        self.assertEqual(response.details, "Failed to connect to the server.")

    def test_disconnect_success(self):
        # Mock a successful disconnection response
        self.mock_client_manager.disconnect.return_value = ConnectionResponse(
            status=ConnectionStatus.OK,
            details="Disconnected successfully."
        )

        # Call the disconnect method
        response = self.modbus_base.disconnect()

        # Assert the disconnect method was called and returned the expected response
        self.mock_client_manager.disconnect.assert_called_once()
        self.assertEqual(response.status, ConnectionStatus.OK)
        self.assertEqual(response.details, "Disconnected successfully.")

    def test_disconnect_failure(self):
        # Mock a failed disconnection response
        self.mock_client_manager.disconnect.return_value = ConnectionResponse(
            status=ConnectionStatus.FAILED,
            details="Client was not connected or was already closed."
        )

        # Call the disconnect method
        response = self.modbus_base.disconnect()

        # Assert the disconnect method was called and returned the expected response
        self.mock_client_manager.disconnect.assert_called_once()
        self.assertEqual(response.status, ConnectionStatus.FAILED)
        self.assertEqual(response.details, "Client was not connected or was already closed.")


if __name__ == '__main__':
    unittest.main()
