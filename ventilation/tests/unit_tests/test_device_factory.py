import os
import random
import string
import tempfile
import unittest
from unittest.mock import MagicMock, patch
import sys
from config.config_factory import ConfigFactory
from config.config_loader import ConfigLoader
from devices.device import Device
from devices.device_factory import DeviceFactory, DeviceStatus, DeviceResponse


class TestDeviceFactory(unittest.TestCase):

    def setUp(self):
        # Clean up registry and sys.modules before each test
        DeviceFactory._registry = {}
        DeviceFactory._dependency = {}
        if 'registered' in sys.modules:
            del sys.modules['registered']

    def test_init_calls_load_registered_devices(self):
        # Ensure registered module is not in sys.modules
        if 'registered' in sys.modules:
            del sys.modules['registered']

        config_factory_mock = MagicMock(spec=ConfigFactory)
        with patch.object(DeviceFactory, '_load_registered_devices') as mock_load:
            DeviceFactory(config_factory_mock)
            mock_load.assert_called_once()

    def test_init_does_not_call_load_registered_devices(self):
        # Simulate that the registered module is already loaded
        sys.modules['registered'] = MagicMock()

        config_factory_mock = MagicMock(spec=ConfigFactory)
        with patch.object(DeviceFactory, '_load_registered_devices') as mock_load:
            DeviceFactory(config_factory_mock)
            mock_load.assert_not_called()

    def test_load_registered_devices_failure(self):
        with patch('importlib.import_module', side_effect=ImportError("Failed")):
            with self.assertRaises(ImportError):
                DeviceFactory._load_registered_devices()

    def test_registered_devices_loaded_true(self):
        sys.modules['registered'] = MagicMock()
        self.assertTrue(DeviceFactory._registered_devices_loaded())
        del sys.modules['registered']  # Clean up

    def test_registered_devices_loaded_false(self):
        if 'registered' in sys.modules:
            del sys.modules['registered']  # Ensure registered module is not loaded
        self.assertFalse(DeviceFactory._registered_devices_loaded())

    def test_register_device(self):
        class TestDevice(Device):
            pass

        DeviceFactory.register_device("TestDevice", TestDevice)
        self.assertIn("TestDevice", DeviceFactory._registry)
        self.assertEqual(DeviceFactory._registry["TestDevice"], TestDevice)

    def test_register_dependency(self):
        class TestDependency:
            pass

        DeviceFactory.register_dependency("TestDependency", TestDependency)
        self.assertIn("TestDependency", DeviceFactory._dependency)
        self.assertEqual(DeviceFactory._dependency["TestDependency"], TestDependency)

    def test_create_device_success(self):
        config_factory_mock = MagicMock(spec=ConfigFactory)
        loader_mock = MagicMock()
        config_factory_mock.create_loader.return_value = loader_mock

        class TestDevice(Device):
            required_dependencies = []

            def __init__(self, config_loader):
                super().__init__(config_loader)
                self.config_loader = config_loader

            @classmethod
            def get_new_name(cls):
                return "my new name"

        DeviceFactory.register_device("TestDevice", TestDevice)
        factory = DeviceFactory(config_factory_mock)
        response: DeviceResponse[TestDevice] = factory.create("TestDevice")

        self.assertEqual(response.status, DeviceStatus.VALID)
        self.assertIsInstance(response.device, TestDevice)
        self.assertEqual(response.device.config_loader, loader_mock)

    def test_create_device_not_registered(self):
        config_factory_mock = MagicMock(spec=ConfigFactory)
        factory = DeviceFactory(config_factory_mock)

        response = factory.create("NonExistentDevice")

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

        DeviceFactory.register_device("TestDevice", TestDevice)
        factory = DeviceFactory(config_factory_mock)
        response = factory.create("TestDevice")

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

        DeviceFactory.register_dependency("test_dependency", TestDependency)

        class TestDevice(Device):
            required_dependencies = ['test_dependency']

            def __init__(self, config_loader, test_dependency):
                super().__init__(config_loader)
                self.config_loader = config_loader
                self.test_dependency = test_dependency

        DeviceFactory.register_device("TestDevice", TestDevice)
        factory = DeviceFactory(config_factory_mock)
        response = factory.create("TestDevice")

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

        DeviceFactory.register_dependency("core_dependency", CoreDependency)

        # Register an extra dependency
        class ExtraDependency:
            pass

        DeviceFactory.register_dependency("extra_dependency", ExtraDependency)

        class TestDevice(Device):
            required_dependencies = ["core_dependency"]

            def __init__(self, config_loader, core_dependency, extra_dependency):
                super().__init__(config_loader)
                self.config_loader = config_loader
                self.core_dependency = core_dependency
                self.extra_dependency = extra_dependency

        DeviceFactory.register_device("TestDevice", TestDevice)
        factory = DeviceFactory(config_factory_mock)
        response = factory.create("TestDevice")

        self.assertEqual(response.status, DeviceStatus.VALID)
        self.assertIsInstance(response.device, TestDevice)
        self.assertIsInstance(response.device.core_dependency, CoreDependency)
        self.assertIsInstance(response.device.extra_dependency, ExtraDependency)

    @classmethod
    def _generate_random_package_name(cls, length=8):
        """Generate a random package name to avoid name conflicts."""
        return 'pkg_' + ''.join(random.choices(string.ascii_lowercase, k=length))

    def test_load_registered_devices_success(self):
        with tempfile.TemporaryDirectory() as tmp_dir_name:
            # Generate a unique package name
            random_package_name = self._generate_random_package_name()

            # Create the random package directory
            package_dir = os.path.join(tmp_dir_name, random_package_name)
            os.mkdir(package_dir)

            # Create empty Python module files in the random package
            with open(os.path.join(package_dir, 'module1.py'), 'w') as f:
                f.write('')  # Empty module file
            with open(os.path.join(package_dir, 'module2.py'), 'w') as f:
                f.write('')  # Empty module file

            # Add the temporary directory to sys.path
            sys.path.insert(0, tmp_dir_name)

            try:
                # Patch the REGISTERED constant to point to the unique package
                with patch('devices.device_factory.REGISTERED', random_package_name):
                    # Call the method to load registered devices
                    DeviceFactory._load_registered_devices()

                    # Check that the modules were loaded into sys.modules
                    self.assertIn(f'{random_package_name}.module1', sys.modules)
                    self.assertIn(f'{random_package_name}.module2', sys.modules)
            finally:
                # Clean up sys.path and sys.modules after the test
                sys.path.pop(0)
                sys.modules.pop(f'{random_package_name}.module1', None)
                sys.modules.pop(f'{random_package_name}.module2', None)
                sys.modules.pop(random_package_name, None)


if __name__ == '__main__':
    unittest.main()
