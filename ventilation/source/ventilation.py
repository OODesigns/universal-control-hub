from utils.temperaturecelsius import TemperatureCelsius, TemperatureInterface
from ventilation_mode import VentilationMode


class Ventilation:
    def __init__(self):
        self.mode = None

    @property
    def mode(self) -> VentilationMode:
        return self._mode

    @mode.setter
    def mode(self, mode: VentilationMode):
        self._mode = mode

    @property
    def mvhr_temp_supply_in(self) -> TemperatureInterface:
        return TemperatureCelsius(0)

    @property
    def mvhr_temp_supply_out(self) -> TemperatureInterface:
        return TemperatureCelsius(0)

    @property
    def set_point_temperature(self) -> TemperatureInterface:
        return TemperatureCelsius(0)

    @set_point_temperature.setter
    def set_point_temperature(self, temp: TemperatureInterface):
        pass
