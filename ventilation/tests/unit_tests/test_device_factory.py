import unittest
from unittest.mock import Mock, patch
from DeviceFactory import DeviceFactory, DEVICES
from devices.device import Device
from store import Store

@DeviceFactory.register_device("Test")
class TestClass(Device):
    pass

class TestDeviceFactory(unittest.TestCase):

    def setUp(self):
        """Set up a mock Store object before each test."""
        self.mock_store = Mock(spec=Store)
        self.factory = DeviceFactory(self.mock_store)

    def test_device_factory_registers_device(self):
        """Test that devices are correctly registered with the factory."""
        device = self.factory.create_device("Test")

        self.assertIsInstance(device, TestClass)
        self.assertEqual(device.store, self.mock_store)

    def test_device_factory_raises_error_on_unknown_device(self):
        """Test that the factory raises an error when an unknown device is requested."""
        with self.assertRaises(ValueError):
            self.factory.create_device("unknown_device")

    @patch('sys.modules')
    def test_registered_devices_loaded_with_modules(self, mock_sys_modules):
        """Test _registered_devices_loaded when DEVICES is in sys.modules."""
        # Arrange
        mock_sys_modules.get.return_value = True

        # Act
        result = self.factory._registered_devices_loaded()

        # Assert
        self.assertTrue(result)
        mock_sys_modules.get.assert_called_once_with(DEVICES)






if __name__ == '__main__':
    unittest.main()
