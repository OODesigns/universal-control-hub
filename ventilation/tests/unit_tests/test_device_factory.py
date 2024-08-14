import unittest
from unittest.mock import Mock
from DeviceFactory import DeviceFactory
from devices.device import Device
from store import Store

@DeviceFactory.register_device("Test")
class TestClass(Device):
    pass

class TestDeviceFactory(unittest.TestCase):

    def setUp(self):
        """Set up a mock Store object before each test."""
        self.mock_store = Mock(spec=Store)

    def test_device_factory_registers_device(self):
        """Test that devices are correctly registered with the factory."""

        factory = DeviceFactory(self.mock_store)

        device = factory.create_device("Test")

        self.assertIsInstance(device, TestClass)
        self.assertEqual(device.store, self.mock_store)






    #
    # def test_device_factory_creates_sensor(self):
    #     """Test that the factory creates a Sensor instance."""
    #     sensor = DeviceFactory.create_device("sensor", self.mock_store)
    #     self.assertIsInstance(sensor, Sensor)
    #     self.assertEqual(sensor.store, self.mock_store)
    #
    # def test_device_factory_creates_mvhr(self):
    #     """Test that the factory creates an MVHR instance."""
    #     mvhr = DeviceFactory.create_device("mvhr", self.mock_store)
    #     self.assertIsInstance(mvhr, MVHR)
    #     self.assertEqual(mvhr.store, self.mock_store)
    #
    # def test_device_factory_raises_error_on_unknown_device(self):
    #     """Test that the factory raises an error when an unknown device is requested."""
    #     with self.assertRaises(ValueError):
    #         DeviceFactory.create_device("unknown_device", self.mock_store)
    #
    # def test_sensor_read_method(self):
    #     """Test that the Sensor's read method works as expected."""
    #     sensor = DeviceFactory.create_device("sensor", self.mock_store)
    #     self.assertEqual(sensor.read(), "Sensor data")
    #
    # def test_mvhr_control_method(self):
    #     """Test that the MVHR's control method works as expected."""
    #     mvhr = DeviceFactory.create_device("mvhr", self.mock_store)
    #     self.assertEqual(mvhr.control(), "MVHR control action")

if __name__ == '__main__':
    unittest.main()
