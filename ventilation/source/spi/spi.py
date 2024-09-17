from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import List

from spi.spi_command import SPICommand
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
    @abstractmethod
    def execute(self, command: SPICommand = None) -> Response:
        """
        Execute an SPICommand, optionally provided. If no command is provided,
        the default behavior for the device will be executed.

        :param command: Optional SPICommand to execute. If None, default command will be used.
        :return: A Response object containing the result.
        """
        pass








