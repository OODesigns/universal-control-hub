from dataclasses import dataclass, field
from abc import ABC, abstractmethod

from spi.spi_values import SPIBusNumber, SPIChipSelect, SPIMaxSpeedHz, SPIMode, SPIBitsPerWord


@dataclass(frozen=True)
class SPIInterface(ABC):
    bus: SPIBusNumber = field(init=False)
    chip_select: SPIChipSelect = field(init=False)
    max_speed_Hz: SPIMaxSpeedHz = field(init=False)
    mode: SPIMode = field(init=False)
    bits_per_word:SPIBitsPerWord = field(init=False)

    def __init__(self, builder):
        from spi.spi_builder import SPIBuilder
        assert isinstance(builder, SPIBuilder), "Expected builder to be an instance of SPIBuilder"
        object.__setattr__(self, 'bus', builder.bus)
        object.__setattr__(self, 'chip_select', builder.chip_select)
        object.__setattr__(self, 'max_speed_hz', builder.max_speed_hz)
        object.__setattr__(self, 'mode', builder.mode)
        object.__setattr__(self, 'bits_per_word', builder.bits_per_word)


    @abstractmethod
    def create_spi_client(self):
        """
        Abstract method to create and return the SPI client.
        This should be implemented in the subclass or specialized module.
        """
        pass  # pragma: no cover

    @abstractmethod
    def transfer(self, data):
        """
        Transfer data to and from the SPI device.
        :param data: A list of bytes to send to the SPI device.
        :return: A list of bytes received from the SPI device.
        """
        pass  # pragma: no cover

    @abstractmethod
    def read(self, nbytes):
        """
        Read a specified number of bytes from the SPI device.
        :param nbytes: Number of bytes to read.
        :return: A list of bytes received from the SPI device.
        """
        pass  # pragma: no cover

    @abstractmethod
    def write(self, data):
        """
        Write data to the SPI device.
        :param data: A list of bytes to send to the SPI device.
        """
        pass  # pragma: no cover

    @abstractmethod
    def close(self):
        """
        Close the SPI connection.
        """
        pass  # pragma: no cover
