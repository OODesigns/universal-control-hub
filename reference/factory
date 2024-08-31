import unittest
from unittest.mock import MagicMock
from config.config_factory import ConfigFactory
from devices.device import Device
from devices.device_factory import DeviceFactory, DeviceStatus


class TestDeviceFactory(unittest.TestCase):

    def setUp(self):
        self.config_factory = MagicMock(spec=ConfigFactory)
        self.factory = DeviceFactory(self.config_factory)

    def test_create_device_not_registered(self):
        response = self.factory.create_device("UnregisteredDevice")
        self.assertEqual(response.status, DeviceStatus.EXCEPTION)
        self.assertEqual(response.details, "Device 'UnregisteredDevice' is not registered.")
        self.assertIsNone(response.device)

    # noinspection PyUnusedLocal
    def test_create_device_missing_dependency(self):
        @DeviceFactory.register_device("TestDevice")
        class TestDevice(Device):
            required_dependencies = ["MissingDependency"]

        response = self.factory.create_device("TestDevice")
        self.assertEqual(response.status, DeviceStatus.EXCEPTION)
        self.assertEqual(response.details, "Dependency 'MissingDependency' is required by TestDevice but not provided.")
        self.assertIsNone(response.device)

    def test_create_device_successful(self):
        @DeviceFactory.register_device("TestDevice")
        class TestDevice(Device):
            required_dependencies = []

            def __init__(self, config_loader, **dependencies):
                super().__init__(config_loader)
                self.config_loader = config_loader
                self.dependencies = dependencies

        response = self.factory.create_device("TestDevice")
        self.assertEqual(response.status, DeviceStatus.VALID)
        self.assertEqual(response.details, "Device TestDevice has been initialized.")
        self.assertIsInstance(response.device, TestDevice)


if __name__ == '__main__':
    unittest.main()
