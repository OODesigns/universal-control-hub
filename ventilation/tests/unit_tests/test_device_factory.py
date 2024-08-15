import unittest
from unittest.mock import Mock, patch, MagicMock

from config.config_factory import ConfigFactory
from devices.device_factory import DeviceFactory, DEVICES
from devices.device import Device

@DeviceFactory.register_device("Test")
class TestClass(Device):
    pass

class TestDeviceFactory(unittest.TestCase):

    def setUp(self):
        """Set up a mock ConfigFactory object before each test."""
        self.mock_config_factory = Mock(spec=ConfigFactory)
        self.factory = DeviceFactory(self.mock_config_factory)

    def test_device_factory_registers_device(self):
        """Test that devices are correctly registered with the factory."""
        device = self.factory.create_device("Test")

        self.assertIsInstance(device, TestClass)
        self.assertEqual(device.store, self.mock_config_factory)

    def test_device_factory_raises_error_on_unknown_device(self):
        """Test that the factory raises an error when an unknown device is requested."""
        with self.assertRaises(ValueError):
            self.factory.create_device("unknown_device")

    @patch.dict('sys.modules', {DEVICES: MagicMock()})
    def test_registered_devices_loaded_with_modules(self):
        """Test _registered_devices_loaded when DEVICES is in sys.modules."""
        self.assertTrue(self.factory._registered_devices_loaded())

    @patch.dict('sys.modules', {}, clear=True)
    def test_registered_devices_loaded_with_modules(self):
        """Test _registered_devices_loaded when DEVICES is NOT in sys.modules."""
        self.assertFalse(self.factory._registered_devices_loaded())

    @patch('devices.device_factory.DeviceFactory._load_registered_devices')
    @patch.dict('sys.modules', {}, clear=True)
    def test_constructor_loads_devices_when_not_loaded(self, mock_load_registered_devices):
        """Test that the constructor loads devices when they are not already loaded."""
        DeviceFactory(self.mock_config_factory)
        mock_load_registered_devices.assert_called_once()

    @patch('devices.device_factory.DeviceFactory._load_registered_devices')
    @patch.dict('sys.modules', {DEVICES: MagicMock()})
    def test_constructor_does_not_load_devices_when_already_loaded(self, mock_load_registered_devices):
        """Test that the constructor does not load devices if they are already loaded."""
        DeviceFactory(self.mock_config_factory)
        mock_load_registered_devices.assert_not_called()


if __name__ == '__main__':
    unittest.main()
