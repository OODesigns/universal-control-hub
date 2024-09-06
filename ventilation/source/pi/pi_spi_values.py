from spi.spi_values import (SPIBusNumber, SPIChipSelect, SPIMaxSpeedHz,
                            SPIBitsPerWord)


class RaspberryPiSPIBus(SPIBusNumber):
    """
    RaspberryPiSPIBus represents the SPI bus number specifically for the Raspberry Pi.
    The Raspberry Pi 5 supports up to 6 SPI buses.
    """
    high_value = 5  # Raspberry Pi 5 has 6 SPI buses, so the range is 0-5.

class RaspberryPiSPIDevice(SPIChipSelect):
    """
    RaspberryPiSPIDevice represents the device (chip select) number on the SPI bus for Raspberry Pi.
    Raspberry Pi typically supports two chip select lines, CE0 and CE1.
    """
    high_value = 1  # Typically, Raspberry Pi uses CE0 (0) and CE1 (1).

class RaspberryPiSPIMaxSpeedHz(SPIMaxSpeedHz):
    """
    RaspberryPiSPIMaxSpeedHz defines the maximum clock speed for the SPI bus on the Raspberry Pi.
    The typical maximum speed is 32 MHz.
    """
    low_value = 500000  # Raspberry Pi typically operates at speeds starting from 500 kHz.
    high_value = 32000000  # 32 MHz is a typical upper limit for Raspberry Pi SPI communication.

class RaspberryPiSPIBitsPerWord(SPIBitsPerWord):
    """
    RaspberryPiSPIBitsPerWord defines the number of bits per word for SPI communication on Raspberry Pi.
    The Raspberry Pi typically uses 8 bits per word, though other configurations may be possible.
    """
    low_value = 8
    high_value = 8  # Standard SPI communication on Raspberry Pi is 8 bits per word.
