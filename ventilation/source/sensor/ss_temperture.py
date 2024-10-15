from sensor.temperture_strategy import ADCToCurrentConversionStrategy, SensorDetection, \
    CurrentToTemperatureConversionStrategy, RestrictedRangeValidationStrategy
from utils.response import Response
from utils.strategies import ExceptionCascade
from utils.temperaturecelsius import TemperatureCelsius

MAX_TEMP = 50
MIN_TEMP = 0

class SSTemperature(TemperatureCelsius):
    def __init__(self, adc_response: Response[int]):
        self._adc_exception_cascade = ExceptionCascade(adc_response)
        super().__init__(adc_response.value)

    """
    SSTemperature class orchestrates the ADC-to-temperature conversion using the defined strategies.

    This class leverages the following strategies:
    1. `ADCToCurrentConversionStrategy` - Converts the raw ADC value to current (mA).
    2. `SensorDetection` - Detects if the sensor is not working (e.g., no sensor or short circuit).
    3. `CurrentToTemperatureConversionStrategy` - Converts the current to temperature (°C).
    4. `RestrictedRangeValidationStrategy` - Validates that the resulting temperature is within the valid range.

    Each of these strategies is applied in sequence, ensuring proper conversion and validation at each stage.

    Methods:
        get__strategies: Returns the list of strategies to be used for processing the temperature.
    """
    def get__strategies(self) -> [TemperatureCelsius]:
        return [
            self._adc_exception_cascade,
            SensorDetection(),                 # Then check for sensor issues using the current
            ADCToCurrentConversionStrategy(),  # First, convert ADC to current
            CurrentToTemperatureConversionStrategy(MIN_TEMP, MAX_TEMP),  # Convert current to temperature
            RestrictedRangeValidationStrategy(MIN_TEMP, MAX_TEMP)  # Finally, validate the temperature range
        ] + super().get__strategies()


