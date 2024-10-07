from config.config_loader import ConfigLoader
from reader.device_reader import DeviceReader
from spi.spi_builder import SPIClientBuilder
from spi.spi_values import SPIChipSelect, SPIBusNumber, SPIMaxSpeedHz, SPIMode, SPIBitsPerWord, SPIDataOrder, \
    SPIFullDuplex, SPIIdleState


class MCP3208(DeviceReader):

    def __init__(self, config_loader: ConfigLoader):
        super().__init__(config_loader)
        self._spi = (
            SPIClientBuilder()
            .set_bus(SPIBusNumber(config_loader.get_value("spi_bus")))
            .set_chip_select(SPIChipSelect(config_loader.get_value("spi_chip_select")))
            .set_max_speed_hz(SPIMaxSpeedHz(500000))
            .set_mode(SPIMode(0))
            .set_bits_per_word(SPIBitsPerWord(8))

            # Would need to check if we can set defaults for these
            .set_data_order(SPIDataOrder('MSP'))
            .set_full_duplex(SPIFullDuplex(True))
            .set_idle_state(SPIIdleState('Low'))

        ).build()

    def read(self) -> int:
        pass
