from utils.response import Response
from utils.status import Status
from utils.temperaturecelsius import LowTemperatureRange, HighTemperatureRange
from utils.value import ValidationStrategy

# Strategy for converting ADC value to temperature (Celsius) for a sensor sending 0-10V
class ADCToTemperatureConversionStrategy(ValidationStrategy):
    """
    Converts the raw ADC value into the corresponding temperature in Celsius.

    The sensor operates within a 0-10V range, and this strategy maps that range to a temperature range
    of min_temp to max_temp (e.g., 0°C to 100°C).

    Since the ADC reference voltage is 4.096V, the input voltage (0-10V) must be scaled to fit within the
    ADC's input range. The conversion is done assuming the scaling is handled externally (e.g., with a resistor
    divider) to bring 0-10V down to 0-4.096V.
    """
    def __init__(self, min_temp: LowTemperatureRange, max_temp: HighTemperatureRange):
        self.max_temp = max_temp.value
        self.min_temp = min_temp.value

    def validate(self, adc_value: int) -> Response:
        try:
            # Ensure the ADC value is within the valid range
            if not (0 <= adc_value <= 4095):
                return Response(status=Status.EXCEPTION, details=f"ADC value {adc_value} is out of range", value=None)

            # Directly map ADC value to temperature
            temperature_c = ((adc_value / 4095) * (self.max_temp - self.min_temp)) + self.min_temp

            return Response(status=Status.OK, details="ADC to temperature conversion successful", value=round(temperature_c, 2))
        except Exception as e:
            return Response(status=Status.EXCEPTION, details=f"ADC to Temperature Conversion error: {e}", value=None)
