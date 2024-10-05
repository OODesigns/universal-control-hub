from abc import ABC, abstractmethod

class SPIDevInterface(ABC):
    """
    Abstract class for SPI clients that defines the basic interface for SPI communication.
    This is used for type checking and ensures that all SPI clients implement the required methods and properties.
    """

    @abstractmethod
    def open(self, bus: int, device: int) -> None: # pragma: no cover
        """
        Connect the SPI client to a specified bus and device.
        :param bus: The SPI bus number.
        :param device: The SPI device number.
        """
        pass

    @abstractmethod
    def close(self) -> None:# pragma: no cover
        """
        Disconnect the SPI client from the system SPI device.
        """
        pass

    @abstractmethod
    def xfer2(self, data: list) -> list:# pragma: no cover
        """
        Perform a SPI transaction and return the response.
        :param data: A list of bytes to send via SPI.
        :return: A list of bytes received from SPI.
        """
        pass

    @property
    @abstractmethod
    def max_speed_hz(self) -> int:# pragma: no cover
        """
        Get or set the maximum speed for SPI communication in Hz.
        """
        pass

    @max_speed_hz.setter
    @abstractmethod
    def max_speed_hz(self, value: int) -> None:# pragma: no cover
        pass

    @property
    @abstractmethod
    def mode(self) -> int:# pragma: no cover
        """
        Get or set the SPI mode (0-3).
        """
        pass

    @mode.setter
    @abstractmethod
    def mode(self, value: int) -> None:# pragma: no cover
        pass

    @property
    @abstractmethod
    def bits_per_word(self) -> int:# pragma: no cover
        """
        Get or set the number of bits per word for SPI communication.
        """
        pass

    @bits_per_word.setter
    @abstractmethod
    def bits_per_word(self, value: int) -> None:# pragma: no cover
        pass

    # noinspection SpellCheckingInspection
    @property
    @abstractmethod
    def cshigh(self) -> bool:# pragma: no cover
        """
        Get or set whether the chip select is active high.
        """
        pass

    # noinspection SpellCheckingInspection
    @cshigh.setter
    @abstractmethod
    def cshigh(self, value: bool) -> None:# pragma: no cover
        pass

    @property
    @abstractmethod
    def loop(self) -> bool:# pragma: no cover
        """
        Get or set the loopback mode for SPI communication.
        """
        pass

    @loop.setter
    @abstractmethod
    def loop(self, value: bool) -> None:# pragma: no cover
        pass

    # noinspection SpellCheckingInspection
    @property
    @abstractmethod
    def lsbfirst(self) -> bool:# pragma: no cover
        """
        Get or set the LSB first property for SPI communication.
        """
        pass

    # noinspection SpellCheckingInspection
    @lsbfirst.setter
    @abstractmethod
    def lsbfirst(self, value: bool) -> None:# pragma: no cover
        pass

    # noinspection SpellCheckingInspection
    @property
    @abstractmethod
    def threewire(self) -> bool:# pragma: no cover
        """
        Get or set the three-wire mode for SPI communication.
        """
        pass

    # noinspection SpellCheckingInspection
    @threewire.setter
    @abstractmethod
    def threewire(self, value: bool) -> None:# pragma: no cover
        pass