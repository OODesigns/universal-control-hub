import unittest
from unittest.mock import MagicMock
from reader.device_reader import DeviceReader
from reader.device_reader_supplier import DeviceReaderSupplier


class TestDeviceReaderSupplier(unittest.TestCase):

    def test_register_and_get_device_reader(self):
        # Arrange: Create a mock DeviceReader subclass
        mock_device_reader_class = MagicMock(spec=DeviceReader)

        # Act: Register the mock class and retrieve an instance
        # noinspection PyTypeChecker
        DeviceReaderSupplier.register_client(mock_device_reader_class)
        device_reader_instance = DeviceReaderSupplier.get("test_channel")

        # Assert: Check that the registered class is instantiated with the correct argument
        mock_device_reader_class.assert_called_once_with("test_channel")  # Ensure the class was instantiated with "test_channel"
        self.assertEqual(device_reader_instance, mock_device_reader_class())  # Verify returned instance is correct

    def test_get_without_registering(self):
        # Act & Assert: Ensure calling get without registering raises an assertion error
        with self.assertRaises(AssertionError) as context:
            DeviceReaderSupplier._client_class = None  # Ensure no class is registered
            DeviceReaderSupplier.get("test_channel")

        self.assertEqual(str(context.exception), "The device reader class has not been assigned")


if __name__ == '__main__':
    unittest.main()
