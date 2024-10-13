from config.config_loader import ConfigLoader
from devices.device import Device
from reader.device_reader import DeviceReader
from spi.spi_builder import SPIClientBuilder
from spi.spi_values import SPIChipSelect, SPIBusNumber, SPIMaxSpeedHz, SPIMode, SPIBitsPerWord
from utils.response import Response


# This is the most common setting for SPI communication. Most microcontrollers and devices,
# including the MCP3208, expect communication in 8-bit (1 byte) chunks.
# Even though the MCP3208 produces 12-bit results,
# you'll still use 8-bit transfers to send commands and receive data. You typically send and
# receive data in three 8-bit chunks
WORD = 8
# CPOL = 0: The clock is idle low (SCLK is low when idle).
# CPHA = 0: Data is captured on the first clock edge (the rising edge).
# Summary: In this mode, the data is sampled on the rising edge of the clock,
# and the clock idles low between transmissions. It is generally more common and often used when data
# is required to be stable and ready for reading on the rising clock edge.
MODE = 0
# Since the MCP3208 can handle a clock as slow as 10 kHz,
# and since we only need to sample every 0.5 seconds,
# using a clock frequency of around 100 kHz or more will give us enough time
# for the ADC to process the data with plenty of margin.
MAX_SPEED = 100000


class MCP3208(Device, DeviceReader):

    def __init__(self, config_loader: ConfigLoader):
        super().__init__(config_loader)
        self._spi = (
            SPIClientBuilder()
            .set_bus(SPIBusNumber(config_loader.get_value("spi_bus")))
            .set_chip_select(SPIChipSelect(config_loader.get_value("spi_chip_select")))
            .set_max_speed_hz(SPIMaxSpeedHz(MAX_SPEED))
            .set_mode(SPIMode(MODE))
            .set_bits_per_word(SPIBitsPerWord(WORD))

        ).build()

    def read(self) -> int:
        data: Response[list[int]] = self._spi.execute()
        return ((data.value[1] & 0x0F) << 8) | data.value[2]
