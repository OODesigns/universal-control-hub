from utils.value import RangeValidatedValue, EnumValidatedValue


class SPIBusNumber(RangeValidatedValue[int]):
    """
    SPIBusNumber represents the SPI bus number.
    SPI devices may have multiple buses. The range is typically determined by the hardware capabilities.
    """

    def __init__(self, value: int):
        # SPI bus numbers are typically in the range of 0 to 7
        super().__init__(value, int, 0, 7)


class SPIChipSelect(RangeValidatedValue[int]):
    """
    SPIChipSelect represents the device (chip select) number on the SPI bus.
    Typically, this is 0 or 1, but some systems may support more chip selects.
    """

    def __init__(self, value: int):
        # Commonly between 0 and 3 for most systems
        super().__init__(value, int, 0, 3)


class SPIMaxSpeedHz(RangeValidatedValue[int]):
    """
    SPIMaxSpeedHz defines the maximum clock speed for the SPI bus.
    The range can vary widely depending on the hardware, from very low speeds for long-distance communication
    to very high speeds for high-speed data transfer.
    """

    def __init__(self, value: int):
        # Clock speed typically ranges from 10 kHz to 50 MHz
        super().__init__(value, int, 10000, 50000000)


class SPIMode(RangeValidatedValue[int]):
    """
    SPIMode defines the SPI mode of operation, which includes clock polarity and phase.
    The mode is represented by a number between 0 and 3, corresponding to SPI modes 0, 1, 2, and 3.
    """

    def __init__(self, value: int):
        # SPI modes are numbered 0 to 3
        super().__init__(value, int, 0, 3)


class SPIBitsPerWord(RangeValidatedValue[int]):
    """
    SPIBitsPerWord defines the number of bits per word used in SPI communication.
    The common values are 8 bits, but some devices use 16 bits, 24 bits, or even 32 bits per word.
    """

    def __init__(self, value: int):
        # Typically between 4 and 32 bits per word
        super().__init__(value, int, 4, 32)


class SPIMSBDataOrder(EnumValidatedValue[bool]):
    """
    Defines whether data is transmitted MSB-first or LSB-first using a string.
    """

    def __init__(self, value: bool):
        # Valid values are true or false
        super().__init__(value, bool, [True, False])


class SPIChannel(RangeValidatedValue[int]):
    """
    SPIChannel represents the valid channel numbers for SPI devices that support multiple channels,
    such as ADCs like MCP3008.
    """

    def __init__(self, value: int):
        # Channel numbers for most SPI ADCs like MCP3008 range from 0 to 7
        super().__init__(value, int, 0, 7)

