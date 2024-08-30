import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from pymodbus.client import ModbusBaseClient

from modbus.pymodbus.modbus_client_manager import ModbusClientManager, ConnectionStatus

class TestModbusBase(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.mock_client = AsyncMock(spec=ModbusBaseClient)
        self.mock_client_manager = ModbusClientManager(client=self.mock_client)

    async def test_connect_success(self):
        self.mock_client.connected = True
        response = await self.mock_client_manager.connect()
        self.assertEqual(response.status, ConnectionStatus.OK)
        self.assertEqual(response.details, "Connected successfully.")

    async def test_connect_failure(self):
        self.mock_client.connected = False
        response = await self.mock_client_manager.connect()
        self.assertEqual(response.status, ConnectionStatus.FAILED)
        self.assertEqual(response.details, "Failed to connect to the server.")

    async def test_connect_exception(self):
        self.mock_client.connect.side_effect = Exception("Connection error")
        response = await self.mock_client_manager.connect()
        self.assertEqual(response.status, ConnectionStatus.EXCEPTION)
        self.assertTrue("Error occurred during connection:" in response.details)

    def test_disconnect_success(self):
        self.mock_client.connected = True
        response = self.mock_client_manager.disconnect()
        self.assertEqual(response.status, ConnectionStatus.OK)
        self.assertEqual(response.details, "Disconnected successfully.")

    def test_disconnect_failure(self):
        self.mock_client.connected = False
        response = self.mock_client_manager.disconnect()
        self.assertEqual(response.status, ConnectionStatus.EXCEPTION)
        self.assertEqual(response.details, "Client was not connected or was already closed.")

    def test_disconnect_exception(self):
        self.mock_client.connected = True
        self.mock_client.close.side_effect = Exception("Disconnection error")
        response = self.mock_client_manager.disconnect()
        self.assertEqual(response.status, ConnectionStatus.EXCEPTION)
        self.assertTrue("Error occurred during disconnect:" in response.details)

if __name__ == '__main__':
    unittest.main()
