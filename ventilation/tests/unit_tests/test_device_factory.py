import unittest
from unittest.mock import MagicMock
from config.config_factory import ConfigFactory
from config.config_loader import ConfigLoader
from devices.device import Device
from devices.device_factory import DeviceFactory, DeviceStatus, DeviceResponse
from utils.standard_name import StandardName


class TestDeviceFactory(unittest.TestCase):

    def setUp(self):
        # Clean up registry before each test
        DeviceFactory._registry = {}
        DeviceFactory._dependency = {}

    def test_register_device(self):
        class TestDevice(Device):
            pass

        device_name = StandardName("test_device")
        DeviceFactory.register_device(device_name, TestDevice)
        self.assertIn(device_name.value, DeviceFactory._registry)
        self.assertEqual(DeviceFactory._registry[device_name.value], TestDevice)

    def test_register_dependency(self):
        class TestDependency:
            pass

        dependency_name = StandardName("test_dependency")
        DeviceFactory.register_dependency(dependency_name, TestDependency)
        self.assertIn(dependency_name.value, DeviceFactory._dependency)
        self.assertEqual(DeviceFactory._dependency[dependency_name.value], TestDependency)

    def test_create_device_success(self):
        config_factory_mock = MagicMock(spec=ConfigFactory)
        loader_mock = MagicMock()
        config_factory_mock.create_loader.return_value = loader_mock

        class TestDevice(Device):
            required_dependencies = []

            def __init__(self, config_loader):
                super().__init__(config_loader)
                self.config_loader = config_loader

        device_name = StandardName("test_device")
        DeviceFactory.register_device(device_name, TestDevice)
        factory = DeviceFactory(config_factory_mock)
        response: DeviceResponse[TestDevice] = factory.create(device_name)

        self.assertEqual(response.status, DeviceStatus.VALID)
        self.assertIsInstance(response.device, TestDevice)
        self.assertEqual(response.device.config_loader, loader_mock)

    def test_create_device_not_registered(self):
        config_factory_mock = MagicMock(spec=ConfigFactory)
        factory = DeviceFactory(config_factory_mock)

        device_name = StandardName("non_existent_device")
        response = factory.create(device_name)

        self.assertEqual(response.status, DeviceStatus.EXCEPTION)
        self.assertIsNone(response.device)
        self.assertIn("not registered", response.details)

    def test_create_device_missing_dependency(self):
        config_loader_mock = MagicMock(spec=ConfigLoader)

        config_factory_mock = MagicMock(spec=ConfigFactory)
        config_factory_mock.create_loader.return_value = config_loader_mock

        config_loader_mock.get_array.return_value = []

        class TestDevice(Device):
            required_dependencies = ['missing']

            def __init__(self, config_loader):
                super().__init__(config_loader)
                self.config_loader = config_loader

        device_name = StandardName("test_device")
        DeviceFactory.register_device(device_name, TestDevice)
        factory = DeviceFactory(config_factory_mock)
        response = factory.create(device_name)

        self.assertEqual(response.status, DeviceStatus.EXCEPTION)
        self.assertIsNone(response.device)
        self.assertIn("Dependency 'missing' is required", response.details)

    def test_create_device_with_dependency(self):
        config_loader_mock = MagicMock(spec=ConfigLoader)

        config_factory_mock = MagicMock(spec=ConfigFactory)
        config_factory_mock.create_loader.return_value = config_loader_mock

        config_loader_mock.get_array.return_value = []

        class TestDependency:
            pass

        dependency_name = StandardName("test_dependency")
        DeviceFactory.register_dependency(dependency_name, TestDependency)

        class TestDevice(Device):
            required_dependencies = [dependency_name.value]

            def __init__(self, config_loader, test_dependency):
                super().__init__(config_loader)
                self.config_loader = config_loader
                self.test_dependency = test_dependency

        device_name = StandardName("test_device")
        DeviceFactory.register_device(device_name, TestDevice)
        factory = DeviceFactory(config_factory_mock)
        response = factory.create(device_name)

        self.assertEqual(response.status, DeviceStatus.VALID)
        self.assertIsInstance(response.device, TestDevice)
        self.assertIsInstance(response.device.test_dependency, TestDependency)

    def test_create_device_with_config_extended_dependencies(self):
        # Mock the configuration to return additional dependencies from a file
        config_factory_mock = MagicMock(spec=ConfigFactory)
        loader_mock = MagicMock(spec=ConfigLoader)
        loader_mock.get_array.return_value = ["extra_dependency"]
        config_factory_mock.create_loader.return_value = loader_mock

        # Register a core dependency
        class CoreDependency:
            pass

        core_dependency_name = StandardName("core_dependency")
        DeviceFactory.register_dependency(core_dependency_name, CoreDependency)

        # Register an extra dependency
        class ExtraDependency:
            pass

        extra_dependency_name = StandardName("extra_dependency")
        DeviceFactory.register_dependency(extra_dependency_name, ExtraDependency)

        class TestDevice(Device):
            required_dependencies = [core_dependency_name.value]

            def __init__(self, config_loader, core_dependency, extra_dependency):
                super().__init__(config_loader)
                self.config_loader = config_loader
                self.core_dependency = core_dependency
                self.extra_dependency = extra_dependency

        device_name = StandardName("test_device")
        DeviceFactory.register_device(device_name, TestDevice)
        factory = DeviceFactory(config_factory_mock)
        response = factory.create(device_name)

        self.assertEqual(response.status, DeviceStatus.VALID)
        self.assertIsInstance(response.device, TestDevice)
        self.assertIsInstance(response.device.core_dependency, CoreDependency)
        self.assertIsInstance(response.device.extra_dependency, ExtraDependency)


if __name__ == '__main__':
    unittest.main()