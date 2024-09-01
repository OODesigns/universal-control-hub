import unittest
from unittest.mock import MagicMock
from config.config_loader import ConfigLoader
from devices.mvhr import MVHR
from mvhr_repository import MVHRRepositoryInterface
from utils.connection_reponse import ConnectionResponse, ConnectionStatus


# Creating a concrete implementation of MVHR for testing
class TestMVHR(MVHR):
    async def read_data(self) -> MVHRRepositoryInterface:
        return MagicMock(spec=MVHRRepositoryInterface)

    async def start(self) -> ConnectionResponse:
        return ConnectionResponse(status=ConnectionStatus.OK, details="Started successfully")

    def stop(self) -> ConnectionResponse:
        return ConnectionResponse(status=ConnectionStatus.OK, details="Stopped successfully")


class MVHRTestCase(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_config_loader = MagicMock(spec=ConfigLoader)
        self.device = TestMVHR(self.mock_config_loader)

    def test_initialization(self):
        self.assertIsInstance(self.device, MVHR)
        self.assertEqual(self.device._config_loader, self.mock_config_loader)

    async def test_start(self):
        response = await self.device.start()
        self.assertIsInstance(response, ConnectionResponse)
        self.assertEqual(response.status, ConnectionStatus.OK)
        self.assertEqual(response.details, "Started successfully")

    async def test_read_data(self):
        data = await self.device.read_data()
        self.assertIsInstance(data, MVHRRepositoryInterface)

    def test_stop(self):
        response = self.device.stop()
        self.assertIsInstance(response, ConnectionResponse)
        self.assertEqual(response.status, ConnectionStatus.OK)
        self.assertEqual(response.details, "Stopped successfully")


class ConnectionResponseTestCase(unittest.TestCase):

    def test_connection_response_ok(self):
        response = ConnectionResponse(status=ConnectionStatus.OK, details="All good")
        self.assertEqual(response.status, ConnectionStatus.OK)
        self.assertEqual(response.details, "All good")

    def test_connection_response_failed(self):
        response = ConnectionResponse(status=ConnectionStatus.FAILED, details="Something went wrong")
        self.assertEqual(response.status, ConnectionStatus.FAILED)
        self.assertEqual(response.details, "Something went wrong")


class MVHRRepositoryInterfaceTestCase(unittest.TestCase):

    def test_temp_supply_in(self):
        repo = MagicMock(spec=MVHRRepositoryInterface)
        self.assertTrue(hasattr(repo, 'temp_supply_in'))

    def test_temp_supply_out(self):
        repo = MagicMock(spec=MVHRRepositoryInterface)
        self.assertTrue(hasattr(repo, 'temp_supply_out'))


if __name__ == '__main__':
    unittest.main()
