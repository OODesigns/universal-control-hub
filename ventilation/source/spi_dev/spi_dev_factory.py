import platform

from spi_dev.spi_mock_client import MockSPI


class SPIDevFactory:
    @staticmethod
    def create():
        """
        Return either the real spidev.SpiDev() or a mock class based on the platform.
        """
        if platform.system().lower() == "linux":
            try:
                import spidev
            except ImportError:
                spidev = None
        else:
            return MockSPI()
