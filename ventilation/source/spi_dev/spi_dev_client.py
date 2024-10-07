from typing import List
from spi.spi_client import SPIClient
from spi.spi_command import SPICommand
from spi_dev.spi_dev_interface import SPIDevInterface
from spi_dev.spi_dev_factory import SPIDevFactory
from utils.response import Response
from utils.status import Status


class SPIDevClient(SPIClient):
    def __init__(self, builder):
        """
        Initialize the SPIDevClient using the builder values to set up the spidev instance.
        :param builder: An SPIClientBuilder object that holds the configuration.
        """
        self.builder = builder
        self.spi: SPIDevInterface = SPIDevFactory.create()
        self.is_open = False

    def open(self):
        """
        Open the SPI connection using values from the builder.
        """
        if not self.is_open:
            self.spi.open(self.builder.bus.value, self.builder.chip_select.value)
            self.spi.max_speed_hz = self.builder.max_speed_hz.value
            self.spi.mode = self.builder.mode.value
            self.spi.bits_per_word = self.builder.bits_per_word.value
            # noinspection SpellCheckingInspection
            self.spi.lsbfirst = (self.builder.data_order.value == 'LSB')
            self.is_open = True

    def execute(self, command: SPICommand = None) -> Response[List[int]]:
        """
        Execute the SPI command. Ensure the connection is open before performing the transfer.
        :param command: The SPICommand to execute.
        :return: A Response object containing the result of the SPI transfer.
        """
        if not self.is_open:
            self.open()

        try:
            # Perform the SPI transfer using xfer2 (transmit and receive simultaneously)
            full_command = command.full_command()  # Get the full command as a list of bytes
            result = self.spi.xfer2(full_command)

            # Return a response object with the result (list of bytes)
            return Response(status=Status.OK, details="Transfer successful", value=result)
        except Exception as e:
            # Handle any exceptions and return an error response
            return Response(status=Status.EXCEPTION, details=str(e), value=[])

    def close(self):
        """
        Close the SPI connection if it is open.
        """
        if self.is_open:
            self.spi.close()
            self.is_open = False
