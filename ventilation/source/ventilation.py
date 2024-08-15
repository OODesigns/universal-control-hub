from devices.device import Device
from utils.temperature import Temperature
from devices.temperature_sensor import AbstractTemperatureSensor
from ventilation_mode import VentilationMode


class Ventilation(Device):
    def __init__(self, outside_temp_sensor: AbstractTemperatureSensor):
        super().__init__()
        self.mode = None
        self.outside_temp_sensor = outside_temp_sensor

    @property
    def mode(self) -> VentilationMode:
        return self._mode

    @mode.setter
    def mode(self, mode: VentilationMode):
        self._mode = mode

    @property
    def mvhr_temp_before(self) -> Temperature:
        return Temperature(0)

    @property
    def mvhr_temp_after(self) -> Temperature:
        return Temperature(0)

    @property
    def setpoint_temperature(self) ->Temperature:
        return Temperature(0)

    @setpoint_temperature.setter
    def setpoint_temperature(self, temp: Temperature):
        pass
