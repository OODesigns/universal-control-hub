from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import List

from spi.spi_values import SPIBusNumber, SPIChipSelect, SPIMaxSpeedHz, SPIMode, SPIBitsPerWord
from utils.operation_response import OperationResponse


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
    def open(self) -> OperationResponse: # pragma: no cover
        """
        Initialize the SPI connection and return an OperationResponse.
        """
    @abstractmethod
    def close(self) -> OperationResponse: # pragma: no cover
        """
        Close the SPI connection and return a CloseResponse.
        """
    # @abstractmethod
    # def transfer(self, data: List[int]) -> List[int]:
    #     """
    #     Perform a full-duplex SPI transfer.
    #     :param data: A list of bytes (0-255) to send.
    #     :return: A list of bytes received during the transfer.
    #     """
    #     # Validate data is in byte range (0-255).
    #     if not all(0 <= byte <= 255 for byte in data):
    #         raise ValueError("All elements in data must be bytes (0-255).")
    #     pass  # Actual transfer logic here.



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


