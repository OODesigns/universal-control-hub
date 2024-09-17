from spi.spi_builder import SPIClientBuilder
from spi.spi_values import SPIChannel


class SPIADCClientBuilder(SPIClientBuilder):
    def __init__(self):
        super().__init__()
        self._channel = None

    def set_channel(self, channel: SPIChannel):
        assert isinstance(channel, SPIChannel), "Invalid channel value"
        self._channel = channel
        return self

class SPI12BITADCBuilder(SPIADCClientBuilder):
    pass
