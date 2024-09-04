from dataclasses import dataclass, field
from abc import ABC, abstractmethod

@dataclass(frozen=True)
class SPIInterface(ABC):
    spi_client: object = field(init=False, default=None)

    def __init__(self,builder):

        from spi.spi_builder import SPIBuilder
        assert isinstance(builder, SPIBuilder), "Expected builder to be an instance of SPIBuilder"
        """
        Post-initialization to set up any necessary clients or perform
        tasks after the dataclass has been created.
        """
        object.__setattr__(self, 'spi_client', self.create_spi_client())

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
