from device import Device
from temperature import Temperature
from temperature_sensor import AbstractTemperatureSensor
from ventilation_mode import VentilationMode


class Ventilation(Device):
    def __init__(self, outside_temp_sensor: AbstractTemperatureSensor):
        super().__init__()
        self.mode = None
        self.outside_temp_sensor = outside_temp_sensor

    def set_mode(self, mode: VentilationMode):
        self.mode = mode

    @property
    def mvhr_temp_before(self) -> Temperature:
        return Temperature(0)

    @property
    def mvhr_temp_after(self) -> Temperature:
        return Temperature(0)

    def set_setpoint_temperature(self, temp: Temperature):
        pass
