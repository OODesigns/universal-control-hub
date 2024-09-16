from dataclasses import replace

from parse import with_pattern

from config.config_loader import ConfigLoader
from devices.temperature_sensor import TemperatureSensorInterface
from spi.spi import SPIInterface
from spi.spi_builder import SPIBuilder
from spi.spi_device_factory import SPIDeviceFactory
from spi_devices.common_devices import ADC_12_BIT
from spi_devices.spi_temperature import SPITemperature
from utils.temperaturecelsius import TemperatureInterface

class TemperatureSensor(TemperatureSensorInterface):
    def __init__(self, config_loader: ConfigLoader, spi_factory: SPIDeviceFactory):
        super().__init__(config_loader)

        #TODO replace with_pattern() that SPI-ADC12BIT-Builder, device=ADC_12_BIT do not needed
        #Do we have a factory at all and the builder is the factory and was register a class
        #into the builder

        spi_builder = (
            SPIBuilder()
            .set_bus(config_loader.get_value("spi_bus"))
            .set_chip_select(config_loader.get_value("spi_chip_select"))
            .set_max_speed_hz(config_loader.get_value("spi_max_speed_hz"))
            .set_mode(config_loader.get_value("spi_mode"))
            .set_bits_per_word(config_loader.get_value("spi_bits_per_word"))
            .set_data_order(config_loader.get_value("spi_data_order"))
            .set_full_duplex(config_loader.get_value("spi_full_duplex"))
            .set_idle_state(config_loader.get_value("spi_idle_state"))

            #opertional So should have this for ADCSPIBuilder only
            .set_channel(config_loader.get_value("spi_channel"))
        )
        self._spi = spi_factory.create(device=ADC_12_BIT, builder=spi_builder)

    @property
    def spi(self) -> SPIInterface:
        return self._spi

    def get_temperature(self) -> TemperatureInterface:
        return SPITemperature(self.spi.execute())
