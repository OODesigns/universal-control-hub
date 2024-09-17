from typing import Type

from spi.spi import SPIInterface
from spi.spi_builder_client import SPIBuilderClient
from spi.spi_values import (SPIBusNumber, SPIChipSelect, SPIMaxSpeedHz,
                            SPIMode, SPIBitsPerWord, SPIDataOrder, SPIFullDuplex, SPIIdleState)


class SPIClientBuilder:
    _client_class: Type[SPIBuilderClient] = None

    @classmethod
    def register_client(cls, client_class: Type[SPIBuilderClient]):
        """
        :type client_class: object
        """
        cls._client_class = client_class

    def __init__(self):
        # Initialize attributes to None or appropriate defaults
        self._bus = None
        self._chip_select = None
        self._max_speed_hz = None
        self._mode = None
        self._bits_per_word = None
        self._data_order = None
        self._full_duplex = None
        self._idle_state = None

    # Properties with getters
    @property
    def bus(self) -> SPIBusNumber:
        return self._bus

    @property
    def chip_select(self) -> SPIChipSelect:
        return self._chip_select

    @property
    def max_speed_hz(self) -> SPIMaxSpeedHz:
        return self._max_speed_hz

    @property
    def mode(self) -> SPIMode:
        return self._mode

    @property
    def bits_per_word(self) -> SPIBitsPerWord:
        return self._bits_per_word

    @property
    def data_order(self) -> SPIDataOrder:
        return self._data_order

    @property
    def full_duplex(self) -> SPIFullDuplex:
        return self._full_duplex

    @property
    def idle_state(self) -> SPIIdleState:
        return self._idle_state

    # Setter methods with validation
    def set_bus(self, bus: SPIBusNumber):
        assert isinstance(bus, SPIBusNumber), "Invalid bus value"
        self._bus = bus
        return self

    def set_chip_select(self, chip_select: SPIChipSelect):
        assert isinstance(chip_select, SPIChipSelect), "Invalid chip select value"
        self._chip_select = chip_select
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

    def set_data_order(self, data_order: SPIDataOrder):
        assert isinstance(data_order, SPIDataOrder), "Invalid data order value"
        self._data_order = data_order
        return self

    def set_full_duplex(self, full_duplex: SPIFullDuplex):
        assert isinstance(full_duplex, SPIFullDuplex), "Invalid duplex mode"
        self._full_duplex = full_duplex
        return self

    def set_idle_state(self, idle_state: SPIIdleState):
        assert isinstance(idle_state, SPIIdleState), "Invalid idle state"
        self._idle_state = idle_state
        return self

        # Method to "build" and return a configured SPI object
    def build(self) -> SPIInterface:
        """
        Builds the SPI configuration and returns it.
        This can be used to create a configured SPI object or return the parameters for the SPI connection.
        """
        # Assert required values
        assert self._bus is not None, "SPI bus not set"
        assert self._chip_select is not None, "SPI chip select not set"
        assert self._max_speed_hz is not None, "SPI max speed not set"
        assert self._mode is not None, "SPI mode not set"
        assert self._bits_per_word is not None, "SPI bits per word not set"
        assert self._data_order is not None, "SPI data order not set"
        assert self._full_duplex is not None, "SPI full_duplex not set"
        assert self._idle_state is not None, "SPI Idle state not set"

        assert self._client_class is not None, "The spi client class has not been assigned "
        # Create the client class with the set values
        return self._client_class(self)









