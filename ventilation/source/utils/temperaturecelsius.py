from utils.value import Value

class TemperatureInterface(Value):
    pass

class TemperatureCelsius(TemperatureInterface):
    def __init__(self, value: float):
        super().__init__()
        if not (-20 <= value <= 50):
            raise ValueError("Temperature must be between -20 and 50°C.")
        self._value = value


