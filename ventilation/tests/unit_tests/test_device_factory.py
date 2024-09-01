import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch
import sys
from config.config_factory import ConfigFactory
from config.config_loader import ConfigLoader
from devices.device import Device
from devices.device_factory import DeviceFactory, DeviceStatus


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

        def test_load_registered_devices_success(self):
            with tempfile.TemporaryDirectory() as tmpdirname:
                # Create a fake package directory structure
                package_dir = os.path.join(tmpdirname, 'registered')
                os.mkdir(package_dir)

                # Create some fake modules in the package
                with open(os.path.join(package_dir, 'module1.py'), 'w') as f:
                    f.write('')  # Empty module file
                with open(os.path.join(package_dir, 'module2.py'), 'w') as f:
                    f.write('')  # Empty module file

                # Add the temporary directory to sys.path
                sys.path.insert(0, tmpdirname)

                try:
                    # 'registered' package should now be available to import
                    DeviceFactory._load_registered_devices()

                    # Check that the modules were loaded
                    self.assertIn('registered.module1', sys.modules)
                    self.assertIn('registered.module2', sys.modules)
                finally:
                    # Clean up sys.path
                    sys.path.pop(0)
                    # Clean up loaded modules
                    sys.modules.pop('registered.module1', None)
                    sys.modules.pop('registered.module2', None)
                    sys.modules.pop('registered', None)

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

        DeviceFactory.register_device("TestDevice", TestDevice)
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
        response = factory.create_device("TestDevice")

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
        response = factory.create_device("TestDevice")

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
        response = factory.create_device("TestDevice")

        self.assertEqual(response.status, DeviceStatus.VALID)
        self.assertIsInstance(response.device, TestDevice)
        self.assertIsInstance(response.device.core_dependency, CoreDependency)
        self.assertIsInstance(response.device.extra_dependency, ExtraDependency)


if __name__ == '__main__':
    unittest.main()
