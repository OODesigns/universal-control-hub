import unittest

from reader.device_reader import DeviceReader
from utils.standard_name import StandardName


class TestDeviceReader(DeviceReader):
    def get_device_name(self) -> str:
        return "adc"

    def __init__(self, device_to_read: str):
        super().__init__(device_to_read)

    def read(self) -> int:
        # Return a mock value for testing purposes
        return 42


class TestDeviceReaderClass(unittest.TestCase):

    def test_device_reader_initialization(self):
        # Arrange: Create an instance of TestDeviceReader
        reader = TestDeviceReader("channel_1")

        # Assert: Check if the device_name and config_name are correctly initialized
        self.assertEqual(reader.get_device_name(), "adc")
        self.assertEqual(reader.get_config_name(), StandardName("adc_channel_1"))

    def test_read_method(self):
        # Arrange: Create an instance of TestDeviceReader
        reader = TestDeviceReader("channel_1")

        # Act: Call the read method
        result = reader.read()

        # Assert: Verify the read method returns the correct value
        self.assertEqual(result, 42)


if __name__ == '__main__':
    unittest.main()

