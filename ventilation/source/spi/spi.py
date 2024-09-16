from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import List

from spi.spi_command import SPICommand
from spi.spi_values import (SPIBusNumber, SPIChipSelect, SPIMaxSpeedHz,
                            SPIMode, SPIBitsPerWord, SPIChannel)
from utils.response import Response

class SPIExecutorInterface(ABC):
    @abstractmethod
    def execute(self, command: SPICommand) -> Response[List[int]]:
        """
        Execute an SPICommand that includes both the command and optional data.
        :param command: The SPICommand to execute.
        :return: A Response object containing the result of the SPI transfer (list of bytes).
        """
        pass

@dataclass(frozen=True)
class SPIInterface(ABC):
    bus: SPIBusNumber = field(init=False)
    chip_select: SPIChipSelect = field(init=False)
    max_speed_Hz: SPIMaxSpeedHz = field(init=False)
    mode: SPIMode = field(init=False)
    bits_per_word:SPIBitsPerWord = field(init=False)
    channel: SPIChannel = field(init=False)
    spi_Executor: SPIExecutorInterface = field(init=False)

    def __init__(self, builder):
        from spi.spi_builder import SPIBuilder
        assert isinstance(builder, SPIBuilder), "Expected builder to be an instance of SPIBuilder"
        object.__setattr__(self, 'bus', builder.bus)
        object.__setattr__(self, 'chip_select', builder.chip_select)
        object.__setattr__(self, 'max_speed_hz', builder.max_speed_hz)
        object.__setattr__(self, 'mode', builder.mode)
        object.__setattr__(self, 'bits_per_word', builder.bits_per_word)
        object.__setattr__(self, 'channel', builder.channel)
        object.__setattr__(self, 'spi_Executor', builder.executor)

    @abstractmethod
    def execute(self, command: SPICommand = None) -> Response:
        """
        Execute an SPICommand, optionally provided. If no command is provided,
        the default behavior for the device will be executed.

        :param command: Optional SPICommand to execute. If None, default command will be used.
        :return: A Response object containing the result of the SPI transfer (list of bytes).
        """
        pass








