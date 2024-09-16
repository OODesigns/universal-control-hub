from spi.spi import SPIInterface, SPIExecutorInterface
from spi.spi_values import (SPIBusNumber, SPIChipSelect, SPIMaxSpeedHz,
                            SPIMode, SPIBitsPerWord, SPIDataOrder, SPIFullDuplex, SPIIdleState, SPIChannel)


class SPIBuilder:
    def __init__(self, builder=None):
        """
        Initializes the SPIBuilder. If a builder is provided, copies values from it.
        Otherwise, initializes default values or None.
        """
        if builder:
            assert isinstance(builder, SPIBuilder), "Expected builder to be an instance of SPIBuilder"
            # Copy values from the provided builder
            self.set_bus(builder.bus)
            self.set_chip_select(builder.chip_select)
            self.set_max_speed_hz(builder.max_speed_hz)
            self.set_mode(builder.mode)
            self.set_bits_per_word(builder.bits_per_word)
            self.set_data_order(builder.data_order)
            self.set_full_duplex(builder.full_duplex)
            self.set_idle_state(builder.idle_state)
            self.set_channel(builder.channel)
        else:
            # Initialize attributes to None or appropriate defaults
            self._bus = None
            self._chip_select = None
            self._max_speed_hz = None
            self._mode = None
            self._bits_per_word = None
            self._data_order = None
            self._full_duplex = None
            self._idle_state = None
            self._channel = None
            self._executor = None
            self._client_class = None

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

    @property
    def channel(self) -> SPIChannel:
        return self._channel

    @property
    def executor(self) -> SPIExecutorInterface:
        return self._executor

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

    def set_channel(self, channel: SPIChannel):
        assert isinstance(channel, SPIChannel), "Invalid channel value"
        self._channel = channel
        return self

    def set_executor(self, executor: SPIExecutorInterface):
        assert isinstance(executor, SPIExecutorInterface), "Invalid SPIExecutorInterface value"
        self._executor = executor
        return self

    def set_client_class(self, client_class: type[SPIInterface]):
        assert isinstance(client_class, type), "Invalid class value"
        self._client_class = client_class
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
        assert self._executor is not None, "SPI executor object not set"

        # Create the client class with the set values
        return self._client_class(self)
