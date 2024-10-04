from abc import ABC, abstractmethod
from spi.spi_command import SPICommand
from utils.response import Response


class SPIInterface(ABC):
    @abstractmethod
    def open(self):
        """
        Open the SPI connection.
        """
        pass

    @abstractmethod
    def close(self):
        """
        Close the SPI connection.
        """
        pass


    @abstractmethod
    def execute(self, command: SPICommand = None) -> Response[int]:
        """
        Execute an SPICommand, optionally provided. If no command is provided,
        the default behavior for the device will be executed.

        :param command: Optional SPICommand to execute. If None, default command will be used.
        :return: A Response object containing the result.
        """
        pass






