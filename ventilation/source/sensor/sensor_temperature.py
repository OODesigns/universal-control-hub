from sensor.temperture_strategy import ADCToCurrentConversionStrategy, SensorDetectionStrategy, \
                                       CurrentToTemperatureConversionStrategy
from utils.response import Response
from utils.strategies import ExceptionCascadeStrategy
from utils.temperaturecelsius import TemperatureCelsius, LowTemperatureRange, HighTemperatureRange

LOW = 0
HIGH = 1

class SensorTemperature(TemperatureCelsius):
    def __init__(self, adc_response: Response[int],
                 temp_low_range: LowTemperatureRange,
                 temp_high_range: HighTemperatureRange):
        self._temp_high_range = temp_high_range
        self._temp_low_range = temp_low_range
        self._adc_exception_cascade = ExceptionCascadeStrategy(adc_response)
        super().__init__(adc_response.value)

    """
    SensorTemperature class orchestrates the ADC-to-temperature conversion using the defined strategies.

    This class leverages the following strategies:
    1. `SensorDetection` - Detects if the sensor is not working (e.g., no sensor or short circuit).
    2. `ADCToCurrentConversionStrategy` - Converts the raw ADC value to current (mA).
    3. `CurrentToTemperatureConversionStrategy` - Converts the current to temperature (°C).
   
    Each of these strategies is applied in sequence, ensuring proper conversion and validation at each stage.

    Methods:
        get__strategies: Returns the list of strategies to be used for processing the temperature.
    """
    def get__strategies(self) -> [TemperatureCelsius]:
        return [
            self._adc_exception_cascade,       # Does the ADC need to cascade an error
            SensorDetectionStrategy(),         # Then check for sensor issues using the current
            ADCToCurrentConversionStrategy(),  # First, convert ADC to current
                                               # Convert current to temperature
            CurrentToTemperatureConversionStrategy(self._temp_low_range.value, self._temp_high_range.value)
        ] + super().get__strategies()


