from utils.value import RangeValidatedValue, StrictValidatedValue

class GenericSPIBus(RangeValidatedValue):
    """
    GenericSPIBus represents the SPI bus number.
    SPI devices may have multiple buses. The range is typically determined by the hardware capabilities.
    """
    valid_types = (int,)
    low_value = 0
    high_value = 7  # Example maximum for general hardware with multiple SPI interfaces.

class GenericSPIDevice(RangeValidatedValue):
    """
    GenericSPIDevice represents the device (chip select) number on the SPI bus.
    Typically, this is 0 or 1, but some systems may support more chip selects.
    """
    valid_types = (int,)
    low_value = 0
    high_value = 3  # Example maximum, some systems might support up to 4 devices.

class GenericSPIMaxSpeedHz(RangeValidatedValue):
    """
    GenericSPIMaxSpeedHz defines the maximum clock speed for the SPI bus.
    The range can vary widely depending on the hardware, from very low speeds for long-distance communication
    to very high speeds for high-speed data transfer.
    """
    valid_types = (int,)
    low_value = 10000  # 10 kHz for low-speed communication.
    high_value = 50000000  # 50 MHz for high-speed communication.

class GenericSPIMode(RangeValidatedValue):
    """
    GenericSPIMode defines the SPI mode of operation, which includes clock polarity and phase.
    The mode is represented by a number between 0 and 3, corresponding to SPI modes 0, 1, 2, and 3.
    """
    valid_types = (int,)
    low_value = 0
    high_value = 3  # SPI modes 0 through 3 are standard.

class GenericSPIBitsPerWord(RangeValidatedValue):
    """
    GenericSPIBitsPerWord defines the number of bits per word used in SPI communication.
    The common values are 8 bits, but some devices use 16 bits, 24 bits, or even 32 bits per word.
    """
    valid_types = (int,)
    low_value = 4   # Some devices may use as few as 4 bits.
    high_value = 32  # Some advanced devices use up to 32 bits per word.
