from typing import Type

from spi.spi import SPIInterface
from spi.spi_values import (SPIBusNumber, SPIChipSelect, SPIMaxSpeedHz,
                            SPIMode, SPIBitsPerWord)


class SPIBuilder:
    def __init__(self, builder=None, client_class: Type[SPIInterface] = None):
        """
        Initializes the SPIBuilder. If a builder is provided, copies values from it.
        Otherwise, initializes default values or None.
        """
        if builder:
            assert isinstance(builder, SPIBuilder), "Expected builder to be an instance of SPIBuilder"
            # Copy values from the provided builder
            self.set_bus(builder.bus)
            self.set_device(builder.device)
            self.set_max_speed_hz(builder.max_speed_hz)
            self.set_mode(builder.mode)
            self.set_bits_per_word(builder.bits_per_word)
        else:
            # Initialize attributes to None or appropriate defaults
            self._bus = None
            self._device = None
            self._max_speed_hz = None
            self._mode = None
            self._bits_per_word = None

        self._client_class = client_class # Store the client class to instantiate later

    # Properties with getters
    @property
    def bus(self) -> SPIBusNumber:
        return self._bus

    @property
    def device(self) -> SPIChipSelect:
        return self._device

    @property
    def max_speed_hz(self) -> SPIMaxSpeedHz:
        return self._max_speed_hz

    @property
    def mode(self) -> SPIMode:
        return self._mode

    @property
    def bits_per_word(self) -> SPIBitsPerWord:
        return self._bits_per_word

    # Setter methods with validation
    def set_bus(self, bus: SPIBusNumber):
        assert isinstance(bus, SPIBusNumber), "Invalid bus value"
        self._bus = bus
        return self

    def set_device(self, device: SPIChipSelect):
        assert isinstance(device, SPIChipSelect), "Invalid device value"
        self._device = device
        return self

    def set_max_speed_hz(self, max_speed_hz: SPIMaxSpeedHz):
        assert isinstance(max_speed_hz, SPIMaxSpeedHz), "Invalid max speed value"
        self._max_speed_hz = max_speed_hz
        return self

    def set_mode(self, mode: SPIMode):
        assert isinstance(mode, SPIMode), "Invalid mode value"
        self._mode = mode
        return self

    def set_bits_per_word(self, bits_per_word: SPIBitsPerWord):
        assert isinstance(bits_per_word, SPIBitsPerWord), "Invalid bits per word value"
        self._bits_per_word = bits_per_word
        return self

    # Method to "build" and return a configured SPI object
    def build(self) -> SPIInterface:
        """
        Builds the SPI configuration and returns it.
        This can be used to create a configured SPI object or return the parameters for the SPI connection.
        """
        assert self._bus is not None, "SPI bus not set"
        assert self._device is not None, "SPI device not set"
        assert self._max_speed_hz is not None, "SPI max speed not set"
        assert self._mode is not None, "SPI mode not set"
        assert self._bits_per_word is not None, "SPI bits per word not set"

        return self._client_class(self)
