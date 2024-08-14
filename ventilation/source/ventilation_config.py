from store import Store
from temperature import Temperature
from ventilation_mode import VentilationMode


class VentilationConfiguration:
    def __init__(self, store: Store):
        self.store = store

    @property
    def ventilation_mode(self) -> VentilationMode:
        return self._ventilation_mode

    @ventilation_mode.setter
    def ventilation_mode(self, value: VentilationMode ):
        self._ventilation_mode = value

    @property
    def setpoint_temperature(self) ->Temperature:
        return self._setpoint_temperature

    @setpoint_temperature.setter
    def setpoint_temperature(self, value: Temperature):
        self._setpoint_temperature = value

