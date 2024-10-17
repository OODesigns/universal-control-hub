from utils.value import RangeValidatedValue, StrictValidatedValue

TEMPERATURE_IN_CELSIUS = "Valid temperature in Celsius"

class TemperatureInterface(RangeValidatedValue[float]):
    pass

class TemperatureCelsius(TemperatureInterface):
    """
    A class that represents and validates temperature in Celsius.
    Ensures the temperature is between -20.0 and 50.0 degrees Celsius.
    """
    def __init__(self, value):
        # Initialize the strategies for type and range validation
        super().__init__(value, (int, float), -20.0, 50.0, TEMPERATURE_IN_CELSIUS)


class StrictTemperatureCelsius(TemperatureCelsius, StrictValidatedValue):
    pass

class LowTemperatureRange(RangeValidatedValue[int]):
    """
    LowTemperatureRange represents the valid temperature range between -20°C and 0°C.
    """
    def __init__(self, value: int):
        super().__init__(value, int, -20, 0)

class HighTemperatureRange(RangeValidatedValue[int]):
    """
    HighTemperatureRange represents the valid temperature range between 40°C and 50°C.
    """
    def __init__(self, value: int):
        super().__init__(value, int, 40, 50)
