from config.config_loader import ConfigLoader
from devices.temperature_sensor import TemperatureSensorInterface
from utils.temperaturecelsius import TemperatureInterface


class TemperatureSensor(TemperatureSensorInterface):
    def __init__(self, config_loader: ConfigLoader):
        super().__init__(config_loader)

    def get_temperature(self) -> TemperatureInterface:
        pass
