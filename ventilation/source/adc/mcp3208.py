from reader.reader import Reader
from spi.spi_12_bit_response_builder import SPI12BitResponseBuilder
from config.config_loader import ConfigLoader
from devices.device import Device
from spi.spi_builder import SPIClientBuilder
from spi.spi_values import SPIChipSelect, SPIBusNumber, SPIMaxSpeedHz, SPIMode, SPIBitsPerWord
from utils.response import Response

"""
  SPIChipSelect represents the device (chip select) number on the SPI bus.
  Typically, this is 0 or 1
"""
CHIP_SELECT = "spi_chip_select"

"""
  SPIBusNumber represents the SPI bus number.
  SPI devices may have multiple buses.Normally 0
"""
BUS = "spi_bus"

"""
  This is the most common setting for SPI communication. Most microcontrollers and devices,
  including the MCP3208, expect communication in 8-bit (1 byte) chunks.
  Even though the MCP3208 produces 12-bit results,
  you'll still use 8-bit transfers to send commands and receive data. You typically send and
  receive data in three 8-bit chunks"
"""
WORD = 8

"""
  CPOL = 0: The clock is idle low (SCLK is low when idle).
  CPHA = 0: Data is captured on the first clock edge (the rising edge).
  Summary: In this mode, the data is sampled on the rising edge of the clock,
  and the clock idles low between transmissions. It is generally more common and often used when data
  is required to be stable and ready for reading on the rising clock edge.
"""
MODE = 0
"""
    Humans typically notice changes in sensor readings in the range of 100 ms to 500 ms. For instance:

    A 100-200 ms response time is generally perceived as instantaneous by most users.
    
    A 500 ms (0.5 seconds) update rate is noticeable but still acceptable for non-critical applications.
    
    Lets update the screen 500ms but back end updates 200ms, so it always to to date

    To read from the MCP3208, a 16-clock cycle SPI transaction is typically required:

    8 bits for command and channel selection.
    8 bits to read the 12-bit result, with 4 bits being dummy data.
    
    This means that the MCP3208 must complete one analog-to-digital conversion in less than 200 ms.
    f = 16 / 0.2 = 80
    
    This is way to low
    
    For reliability and to allow for additional processing or latency, use a higher SPI clock speed, 
    such as 500 kHz to 1 MHz. 
    
    This would provide enough headroom for additional 
    reads and any latency in your microcontroller’s handling of the data.    
    
"""
MAX_SPEED = 500000

class MCP3208(Device, Reader[int]):

    def __init__(self, config_loader: ConfigLoader):
        super().__init__(config_loader)
        self._spi = (
            SPIClientBuilder()
            .set_bus(SPIBusNumber(config_loader.get_value(BUS)))
            .set_chip_select(SPIChipSelect(config_loader.get_value(CHIP_SELECT)))
            .set_max_speed_hz(SPIMaxSpeedHz(MAX_SPEED))
            .set_mode(SPIMode(MODE))
            .set_bits_per_word(SPIBitsPerWord(WORD))

        ).build()

    def read(self) -> Response[int]:
        return SPI12BitResponseBuilder(self._spi.execute()).get_12_bit_result()


