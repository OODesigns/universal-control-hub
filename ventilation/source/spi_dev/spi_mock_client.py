from spi_dev.spi_client_interface import SPIDevClientInterface


class MockSPIClient(SPIDevClientInterface):
    """
    This class simulates the behavior of an SPI client for an MCP3208 ADC.
    Instead of calculating ADC values on the fly, it uses a precomputed table based on current-to-voltage-to-ADC calculations.
    """

    def __init__(self):
        self.opened = False
        self._max_speed_hz = None
        self._mode = None
        self._bits_per_word = None
        self._loop = False
        # noinspection SpellCheckingInspection
        self._cshigh = False
        # noinspection SpellCheckingInspection
        self._lsbfirst = False
        # noinspection SpellCheckingInspection
        self._threewire = False
        # Precomputed table of ADC values for each channel
        self.adc_values = {
            0: 819,   # 4 mA -> 1V -> ADC value ~819
            1: 1287,  # 6.2857 mA -> 1.5714V -> ADC value ~1287
            2: 1756,  # 8.5714 mA -> 2.1428V -> ADC value ~1756
            3: 2225,  # 10.8571 mA -> 2.7142V -> ADC value ~2225
            4: 2694,  # 13.1428 mA -> 3.2857V -> ADC value ~2694
            5: 3163,  # 15.4285 mA -> 3.8571V -> ADC value ~3163
            6: 3631,  # 17.7142 mA -> 4.4285V -> ADC value ~3631
            7: 4095   # 20 mA -> 5V -> ADC value 4095
        }

    def open(self, _bus, _device):
        """
        Simulate opening the SPI connection.
        The `_bus` and `_device` parameters are ignored as they are not needed in the mock.
        """
        if self.opened:
            raise RuntimeError("SPI bus is already open.")
        self.opened = True

    def close(self):
        """
        Simulate closing the SPI connection.
        """
        if not self.opened:
            raise RuntimeError("SPI connection is not open.")
        self.opened = False

    def xfer2(self, data):
        """
        Simulate an SPI transfer.
        This method processes an SPI command and returns a precomputed ADC result.

        The MCP3208 command has the following format:
        - Byte 1: Start bit (always 0x01)
        - Byte 2: Channel configuration (single-ended or differential + channel selection)
        - Byte 3: Dummy byte (0x00)

        The method returns the 12-bit ADC result as 3 bytes.
        """
        if not self.opened:
            raise RuntimeError("SPI connection is not open.")
        if len(data) != 3 or data[0] != 0x01:
            raise ValueError("Invalid SPI command format.")

        # Extract the channel (bits 6-4 from the second byte)
        channel = (data[1] >> 4) & 0x07
        single_ended = (data[1] & 0x08) != 0  # Check if the single-ended bit is set

        # Validate single-ended configuration (assuming the mock only supports single-ended mode)
        if not single_ended:
            raise ValueError("Only single-ended mode is supported in this mock.")

        # Retrieve the precomputed ADC value for the specified channel
        adc_value = self.adc_values.get(channel, 0)

        # Convert the 12-bit ADC value into two bytes
        high_byte = (adc_value >> 8) & 0x0F  # The upper 4 bits
        low_byte = adc_value & 0xFF  # The lower 8 bits

        return [0x00, high_byte, low_byte]  # Return the simulated response

    @property
    def max_speed_hz(self):
        return self._max_speed_hz

    @max_speed_hz.setter
    def max_speed_hz(self, value):
        if value <= 0:
            raise ValueError("Invalid max_speed_hz value.")
        self._max_speed_hz = value

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        if value not in range(4):
            raise ValueError("Invalid SPI mode value. Must be between 0 and 3.")
        self._mode = value

    @property
    def bits_per_word(self):
        return self._bits_per_word

    @bits_per_word.setter
    def bits_per_word(self, value):
        if value not in range(8, 17):
            raise ValueError("Invalid bits_per_word value. Must be between 8 and 16.")
        self._bits_per_word = value

    # noinspection SpellCheckingInspection
    @property
    def cshigh(self):
        return self._cshigh

    # noinspection SpellCheckingInspection
    @cshigh.setter
    def cshigh(self, value):
        if not isinstance(value, bool):
            raise ValueError("cshigh must be a boolean value.")
        self._cshigh = value

    @property
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, value):
        if not isinstance(value, bool):
            raise ValueError("loop must be a boolean value.")
        self._loop = value

    # noinspection SpellCheckingInspection
    @property
    def lsbfirst(self):
        return self._lsbfirst

    # noinspection SpellCheckingInspection
    @lsbfirst.setter
    def lsbfirst(self, value):
        if not isinstance(value, bool):
            raise ValueError("lsbfirst must be a boolean value.")
        self._lsbfirst = value

    # noinspection SpellCheckingInspection
    @property
    def threewire(self):
        return self._threewire

    # noinspection SpellCheckingInspection
    @threewire.setter
    def threewire(self, value):
        if not isinstance(value, bool):
            raise ValueError("threewire must be a boolean value.")
        self._threewire = value

