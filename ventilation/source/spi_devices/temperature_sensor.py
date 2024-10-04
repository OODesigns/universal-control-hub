from config.config_loader import ConfigLoader
from devices.temperature_sensor import TemperatureSensorInterface
from spi.spi import SPIInterface
from spi.spi_builder import SPIClientBuilder
from spi.spi_values import SPIBusNumber, SPIChipSelect, SPIMaxSpeedHz, SPIMode, SPIBitsPerWord
from spi_devices.spi_temperature import SPITemperature
from utils.temperaturecelsius import TemperatureInterface

class TemperatureSensor(TemperatureSensorInterface):
    def __init__(self, config_loader: ConfigLoader):
        super().__init__(config_loader)

        self._spi = (
            SPIClientBuilder()
            .set_bus(SPIBusNumber(config_loader.get_value("spi_bus")))
            .set_chip_select(SPIChipSelect(config_loader.get_value("spi_chip_select")))
            .set_max_speed_hz(SPIMaxSpeedHz(config_loader.get_value("spi_max_speed_hz")))
            .set_mode(SPIMode(config_loader.get_value("spi_mode")))
            .set_bits_per_word(SPIBitsPerWord(config_loader.get_value("spi_bits_per_word")))

            # Would need to check if we can set defaults for these
            .set_data_order(config_loader.get_value("spi_data_order"))
            .set_full_duplex(config_loader.get_value("spi_full_duplex"))
            .set_idle_state(config_loader.get_value("spi_idle_state"))

        ).build()

    @property
    def spi(self) -> SPIInterface:
        return self._spi

    def get_temperature(self) -> TemperatureInterface:
        return SPITemperature(self.spi.execute())
