import unittest
from unittest.mock import patch, MagicMock
from adc.mpc3208_device_reader import MPC3208DeviceReader, ADC
from utils.standard_name import sn


class TestMPC3208DeviceReader(unittest.TestCase):

    @patch('adc.mpc3208_device_reader.DeviceFactory')
    def test_read(self, mock_device_factory):
        # Arrange: Mock the DeviceReader and its read method
        mock_device = MagicMock()
        mock_device.read.return_value = 1234  # Mock return value of the read method
        mock_device_factory.get_device.return_value.device = mock_device

        # Act: Instantiate MPC3208DeviceReader and call the read method
        reader = MPC3208DeviceReader("test_channel")
        result = reader.read()

        # Assert: Ensure the read method was called and returned the correct value
        mock_device.read.assert_called_once()
        self.assertEqual(result, 1234)
        mock_device_factory.get_device.assert_called_once_with(sn(ADC), reader.get_config_name())


if __name__ == '__main__':
    unittest.main()
