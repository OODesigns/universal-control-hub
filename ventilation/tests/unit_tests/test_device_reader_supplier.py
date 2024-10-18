import unittest
from typing import cast
from unittest.mock import MagicMock
from reader.device_reader import DeviceReader
from reader.device_reader_supplier import DeviceReaderSupplier
from utils.response import Response
from utils.standard_name import sn, StandardName
from utils.status import Status


# Define a standalone test class for DeviceReader that returns int
class TestIntDeviceReader(DeviceReader[int]):
    def __init__(self, device_to_read: StandardName):
        super().__init__(device_to_read)

    def get_device_name(self) -> str:
        return "test_int_device"

    def read(self) -> Response[int]:
        return Response[int](Status.OK, details="", value=42)


class TestDeviceReaderSupplier(unittest.TestCase):

    def test_register_and_get_device_reader(self):
        # Arrange: Create a mock DeviceReader subclass
        mock_device_reader_class = MagicMock(spec=DeviceReader)

        # Act: Register the mock class and retrieve an instance
        # noinspection PyTypeChecker
        DeviceReaderSupplier.register_reader(mock_device_reader_class)
        name = sn("test_channel")
        device_reader_instance = DeviceReaderSupplier.get(name)

        # Assert: Check that the registered class is instantiated with the correct argument
        mock_device_reader_class.assert_called_once_with(name)  # Ensure the class was instantiated with "test_channel"
        self.assertEqual(device_reader_instance, mock_device_reader_class())  # Verify returned instance is correct

    def test_get_without_registering(self):
        # Act & Assert: Ensure calling get without registering raises an assertion error
        with self.assertRaises(AssertionError) as context:
            DeviceReaderSupplier._reader_class = None  # Ensure no class is registered
            name = sn("test_channel")
            DeviceReaderSupplier.get(name)

        self.assertEqual(str(context.exception), "The device reader class has not been assigned")


    def test_register_int_device_reader(self):
        # Arrange: Register the TestIntDeviceReader
        DeviceReaderSupplier[int].register_reader(TestIntDeviceReader)

        # Act: Get an instance of the TestIntDeviceReader
        device_reader_instance = DeviceReaderSupplier[int].get(StandardName("int_device"))

        cast(DeviceReaderSupplier, DeviceReaderSupplier[int]).get(StandardName("int_device"))

        # Assert: Check that the returned instance is of type TestIntDeviceReader
        self.assertIsInstance(device_reader_instance, TestIntDeviceReader)
        self.assertEqual(device_reader_instance.get_device_name(), "test_int_device")
        self.assertIsInstance(device_reader_instance.read().value, int)  # Ensure the read value is an integer


if __name__ == '__main__':
    unittest.main()
