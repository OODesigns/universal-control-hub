from dataclasses import dataclass
from spi.spi import SPIReadInterface, SPITransfer
from spi.spi_values import SPIBusNumber, SPIChipSelect, SPIMaxSpeedHz, SPIMode, SPIBitsPerWord, SPIChannel
from utils.response import Response
from utils.status import Status

@dataclass(frozen=True)
class MCP3008(SPIReadInterface):
    bus: SPIBusNumber
    chip_select: SPIChipSelect
    max_speed_Hz: SPIMaxSpeedHz
    mode: SPIMode
    bits_per_word: SPIBitsPerWord
    channel: SPIChannel
    spi_transfer: SPITransfer

    def read(self) -> Response[int]:
        """Read the ADC value from the pre-configured channel."""
        try:
            command = [1, (8 + self.channel.value) << 4, 0]  # Command to read from the correct channel
            response = self.spi_transfer.transfer(command)
            adc_value = ((response[1] & 3) << 8) + response[2]
            return Response(status=Status.OK, details="Read successful", value=adc_value)
        except Exception as e:
            return Response(status=Status.EXCEPTION, details=str(e), value=None)
