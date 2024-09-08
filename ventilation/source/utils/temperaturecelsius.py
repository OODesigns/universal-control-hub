from utils.value import StrictValidatedValue, RangeValidatedValue, TypeValidationStrategy, RangeValidationStrategy

class TemperatureInterface(RangeValidatedValue[float]):
    pass

class TemperatureCelsius(TemperatureInterface):
    """
    A class that represents and validates temperature in Celsius.
    Ensures the temperature is between -20.0 and 50.0 degrees Celsius.
    """
    def __init__(self, value):
        # Initialize the strategies for type and range validation
        super().__init__(value, (int, float), -20.0, 50.0)

class StrictTemperatureCelsius(StrictValidatedValue, TemperatureCelsius):
    pass
