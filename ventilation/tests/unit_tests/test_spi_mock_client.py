import unittest

from spi_dev.spi_mock_client import MockSPIClient


class TestMockSPIClient(unittest.TestCase):

    def setUp(self):
        """
        Set up the mock SPI client for testing.
        """
        self.spi_client = MockSPIClient()
        # Open the SPI connection with bus and device parameters
        self.bus = 0
        self.device = 0
        self.spi_client.open(self.bus, self.device)

    def tearDown(self):
        """
        Close the SPI client after each test.
        """
        self.spi_client.close()

    def test_spi_open_close(self):
        """
        Test opening and closing the SPI connection.
        """
        self.spi_client.close()
        self.assertFalse(self.spi_client.opened, "SPI client should be closed.")
        self.spi_client.open(self.bus, self.device)
        self.assertTrue(self.spi_client.opened, "SPI client should be open.")

    def test_valid_command_single_ended(self):
        """
        Test sending a valid command in single-ended mode for each channel.
        """
        for channel in range(8):
            with self.subTest(channel=channel):
                command = [0x01, (0x88 | (channel << 4)), 0x00]  # Single-ended command for each channel
                response = self.spi_client.xfer2(command)
                adc_value = ((response[1] & 0x0F) << 8) | response[2]
                expected_value = self.spi_client.adc_values[channel]
                self.assertEqual(adc_value, expected_value, f"Channel {channel} ADC value mismatch.")

    def test_invalid_command_not_single_ended(self):
        """
        Test sending an invalid command where the single-ended bit is not set.
        """
        for channel in range(8):
            with self.subTest(channel=channel):
                command = [0x01, (0x00 | (channel << 4)), 0x00]  # Differential mode command (not supported in mock)
                with self.assertRaises(ValueError) as context:
                    self.spi_client.xfer2(command)
                self.assertEqual(str(context.exception), "Only single-ended mode is supported in this mock.")

    def test_invalid_command_format(self):
        """
        Test sending an invalid command format.
        """
        invalid_commands = [
            [0x00, 0x88, 0x00],  # Invalid start bit
            [0x01, 0x88],         # Incomplete command
            [0x01, 0x88, 0x00, 0x00]  # Extra byte in command
        ]
        for command in invalid_commands:
            with self.subTest(command=command):
                with self.assertRaises(ValueError) as context:
                    self.spi_client.xfer2(command)
                self.assertEqual(str(context.exception), "Invalid SPI command format.")

    def test_spi_max_speed_hz(self):
        """
        Test setting the maximum speed for SPI communication.
        """
        self.spi_client.max_speed_hz = 50000
        self.assertEqual(self.spi_client.max_speed_hz, 50000, "SPI max speed should be set correctly.")

    def test_spi_mode(self):
        """
        Test setting the SPI mode (mode 0-3).
        """
        for mode in range(4):
            with self.subTest(mode=mode):
                self.spi_client.mode = mode
                self.assertEqual(self.spi_client.mode, mode, f"SPI mode should be set to {mode}.")

    def test_spi_bits_per_word(self):
        """
        Test setting the number of bits per word for SPI communication.
        """
        self.spi_client.bits_per_word = 8
        self.assertEqual(self.spi_client.bits_per_word, 8, "SPI bits per word should be set correctly.")

    def test_spi_cshigh(self):
        """
        Test setting the chip select high property for SPI communication.
        """
        self.spi_client.cshigh = True
        self.assertTrue(self.spi_client.cshigh, "SPI cshigh should be set to True.")
        self.spi_client.cshigh = False
        self.assertFalse(self.spi_client.cshigh, "SPI cshigh should be set to False.")

    def test_spi_loop(self):
        """
        Test setting the loopback mode for SPI communication.
        """
        self.spi_client.loop = True
        self.assertTrue(self.spi_client.loop, "SPI loop should be set to True.")
        self.spi_client.loop = False
        self.assertFalse(self.spi_client.loop, "SPI loop should be set to False.")

    # noinspection SpellCheckingInspection
    def test_spi_lsbfirst(self):
        """
        Test setting the LSB first property for SPI communication.
        """
        self.spi_client.lsbfirst = True
        self.assertTrue(self.spi_client.lsbfirst, "SPI lsbfirst should be set to True.")
        self.spi_client.lsbfirst = False
        self.assertFalse(self.spi_client.lsbfirst, "SPI lsbfirst should be set to False.")

    # noinspection SpellCheckingInspection
    def test_spi_threewire(self):
        """
        Test setting the three-wire mode for SPI communication.
        """
        self.spi_client.threewire = True
        self.assertTrue(self.spi_client.threewire, "SPI threewire should be set to True.")
        self.spi_client.threewire = False
        self.assertFalse(self.spi_client.threewire, "SPI threewire should be set to False.")

    def test_invalid_max_speed_hz(self):
        """
        Test setting an invalid max speed for SPI communication.
        """
        with self.assertRaises(ValueError) as context:
            self.spi_client.max_speed_hz = -1  # Invalid speed
        self.assertEqual(str(context.exception), "Invalid max_speed_hz value.")

    def test_invalid_spi_mode(self):
        """
        Test setting an invalid SPI mode (must be 0-3).
        """
        with self.assertRaises(ValueError) as context:
            self.spi_client.mode = 5  # Invalid mode
        self.assertEqual(str(context.exception), "Invalid SPI mode value. Must be between 0 and 3.")

    def test_invalid_bits_per_word(self):
        """
        Test setting an invalid number of bits per word.
        """
        with self.assertRaises(ValueError) as context:
            self.spi_client.bits_per_word = 17  # Invalid bits per word (should be between 8 and 16)
        self.assertEqual(str(context.exception), "Invalid bits_per_word value. Must be between 8 and 16.")

if __name__ == "__main__":
    unittest.main()