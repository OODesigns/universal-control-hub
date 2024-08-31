import unittest
from unittest.mock import MagicMock
import sys

from config.config_factory import ConfigFactory
from devices.device_factory import DeviceFactory, DeviceStatus


class TestDeviceFactory(unittest.TestCase):

    def setUp(self):
        # Clean up registry and sys.modules before each test
        DeviceFactory._registry = {}
        DeviceFactory._dependency = {}
        if 'devices' in sys.modules:
            del sys.modules['devices']

    def test_init_calls_load_registered_devices(self):
        # Ensure devices module is not in sys.modules
        if 'devices' in sys.modules:
            del sys.modules['devices']

        config_factory_mock = MagicMock(spec=ConfigFactory)
        DeviceFactory(config_factory_mock)

        # Verify that the devices module was imported
        self.assertIn('devices', sys.modules)

    def test_init_does_not_call_load_registered_devices(self):
        # Simulate that the devices module is already loaded
        sys.modules['devices'] = MagicMock()

        config_factory_mock = MagicMock(spec=ConfigFactory)
        DeviceFactory(config_factory_mock)

        # Since devices were already loaded, _load_registered_devices should not trigger a new import
        self.assertEqual(sys.modules['devices'], sys.modules['devices'])

    def test_load_registered_devices(self):
        # Simulate the devices module not being loaded
        if 'devices' in sys.modules:
            del sys.modules['devices']

        DeviceFactory._load_registered_devices()

        # Check if the module was loaded
        self.assertIn('devices', sys.modules)

    def test_registered_devices_loaded_true(self):
        sys.modules['devices'] = MagicMock()
        self.assertTrue(DeviceFactory._registered_devices_loaded())
        del sys.modules['devices']  # Clean up

    def test_registered_devices_loaded_false(self):
        if 'devices' in sys.modules:
            del sys.modules['devices']  # Ensure devices module is not loaded
        self.assertFalse(DeviceFactory._registered_devices_loaded())

    def test_register_device_decorator(self):
        @DeviceFactory.register_device("TestDevice")
        class TestDevice:
            pass

        self.assertIn("TestDevice", DeviceFactory._registry)
        self.assertEqual(DeviceFactory._registry["TestDevice"], TestDevice)

    def test_register_dependency_decorator(self):
        @DeviceFactory.register_dependency("TestDependency")
        class TestDependency:
            pass

        self.assertIn("TestDependency", DeviceFactory._dependency)
        self.assertEqual(DeviceFactory._dependency["TestDependency"], TestDependency)

    def test_create_device_success(self):
        config_factory_mock = MagicMock(spec=ConfigFactory)
        loader_mock = MagicMock()
        config_factory_mock.create_loader.return_value = loader_mock

        @DeviceFactory.register_device("TestDevice")
        class TestDevice:
            required_dependencies = []

            def __init__(self, config_loader):
                self.config_loader = config_loader

        factory = DeviceFactory(config_factory_mock)
        response = factory.create_device("TestDevice")

        self.assertEqual(response.status, DeviceStatus.VALID)
        self.assertIsInstance(response.device, TestDevice)
        self.assertEqual(response.device.config_loader, loader_mock)

    def test_create_device_not_registered(self):
        config_factory_mock = MagicMock(spec=ConfigFactory)
        factory = DeviceFactory(config_factory_mock)

        response = factory.create_device("NonExistentDevice")

        self.assertEqual(response.status, DeviceStatus.EXCEPTION)
        self.assertIsNone(response.device)
        self.assertIn("not registered", response.details)

    def test_create_device_missing_dependency(self):
        config_factory_mock = MagicMock(spec=ConfigFactory)

        @DeviceFactory.register_device("TestDevice")
        class TestDevice:
            required_dependencies = ['missing']

            def __init__(self, config_loader, missing):
                self.config_loader = config_loader

        factory = DeviceFactory(config_factory_mock)
        response = factory.create_device("TestDevice")

        self.assertEqual(response.status, DeviceStatus.EXCEPTION)
        self.assertIsNone(response.device)
        self.assertIn("Dependency 'missing' is required", response.details)

    def test_create_device_with_dependency(self):
        config_factory_mock = MagicMock(spec=ConfigFactory)
        dependency_mock = MagicMock()

        @DeviceFactory.register_dependency("test_dependency")
        class TestDependency:
            pass

        @DeviceFactory.register_device("TestDevice")
        class TestDevice:
            required_dependencies = ['test_dependency']

            def __init__(self, config_loader, test_dependency):
                self.config_loader = config_loader
                self.test_dependency = test_dependency

        factory = DeviceFactory(config_factory_mock)
        response = factory.create_device("TestDevice")

        self.assertEqual(response.status, DeviceStatus.VALID)
        self.assertIsInstance(response.device, TestDevice)
        self.assertIsInstance(response.device.test_dependency, TestDependency)

if __name__ == '__main__':
    unittest.main()
