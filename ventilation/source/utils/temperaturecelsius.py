from utils.value import StrictValidatedValue, RangeValidatedValue


class TemperatureInterface(RangeValidatedValue):
    pass

class TemperatureCelsius(TemperatureInterface):
        valid_types = (int, float)
        low_value = -20.0
        high_value = 50.0

class StrictTemperatureCelsius(StrictValidatedValue, TemperatureCelsius):
    pass