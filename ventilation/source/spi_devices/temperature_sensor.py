from config.config_loader import ConfigLoader
from devices.temperature_sensor import TemperatureSensorInterface
from spi.spi import SPIInterface
from spi.spi_adc_builder import SPI12BITADCBuilder
from spi_devices.spi_temperature import SPITemperature
from utils.temperaturecelsius import TemperatureInterface

class TemperatureSensor(TemperatureSensorInterface):
    def __init__(self, config_loader: ConfigLoader):
        super().__init__(config_loader)

        self._spi = (
            SPI12BITADCBuilder()
            .set_bus(config_loader.get_value("spi_bus"))
            .set_chip_select(config_loader.get_value("spi_chip_select"))
            .set_max_speed_hz(config_loader.get_value("spi_max_speed_hz"))
            .set_mode(config_loader.get_value("spi_mode"))
            .set_bits_per_word(config_loader.get_value("spi_bits_per_word"))
            .set_data_order(config_loader.get_value("spi_data_order"))
            .set_full_duplex(config_loader.get_value("spi_full_duplex"))
            .set_idle_state(config_loader.get_value("spi_idle_state"))

             # ADC only, channel selection
            .set_channel(config_loader.get_value("spi_channel"))
        ).build()

    @property
    def spi(self) -> SPIInterface:
        return self._spi

    def get_temperature(self) -> TemperatureInterface:
        return SPITemperature(self.spi.execute())
