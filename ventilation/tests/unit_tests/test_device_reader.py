import unittest
from unittest.mock import MagicMock

from config.config_factory import ConfigFactory
from config.config_loader import ConfigLoader
from reader.device_reader import DeviceReader


class TestDeviceReader(unittest.TestCase):
    def test_config_name_for_reader(self):
        config_loader_mock = MagicMock(spec=ConfigLoader)

        config_factory_mock = MagicMock(spec=ConfigFactory)
        config_factory_mock.create_loader.return_value = config_loader_mock

        config_loader_mock.get_array.return_value = []