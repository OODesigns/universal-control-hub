from utils.response import Response
from utils.status import Status
from utils.temperaturecelsius import LowTemperatureRange, HighTemperatureRange
from utils.value import ValidationStrategy

"""
At 20mA, the voltage across the 200-ohm resistor is:
  V = I * R -> 0.02 * 200 = 4.0V
  ADC = V / Vref * (ADC resolution - 1) -> (4 / 4.096) * 4095 = 3999 - rounded down
  This is approximately 2.34% lower than the previous 4.096V to allow better short circuit detection.

At 4mA, the voltage across the 200-ohm resistor is:
  V = I * R -> 0.004 * 200 = 0.8V
  ADC = V / Vref * (ADC resolution - 1) -> (0.8 / 4.096) * 4095 = 800 - rounded up  

For short circuit and open circuit detection with 4.096V reference:
  - Short circuit (20mA expected): ADC value at 4.0V is adjusted to detect short circuits effectively.
  - Open circuit (4mA expected): The voltage across the resistor at 0.8V gives an approximate ADC value of 800.
"""

# Constants for 4-20mA to temperature conversion with a 200-ohm resistor
MIN_CURRENT_MA = 4.0
MAX_CURRENT_MA = 20.0
VOLTAGE_REF = 4.096  # Updated reference voltage
ADC_RESOLUTION = 4096  # 12-bit ADC (MCP3208)
HIGH_VALUE = 3999  # ADC value at approximately 4.0V with 200-ohm resistor
LOW_VALUE = 800  # ADC value at 0.8V (4mA) with 200-ohm resistor
# Allow 1% tolerance
LOW_THRESHOLD = 792  # Rounding Down
HIGH_THRESHOLD = 4039  # Rounding up
ADC_OFF_SET = 1
CONVERT_TO_MA = 1000.0
RESISTOR = 200.0

# Error messages
NO_SENSOR_DETECTED = "No sensor detected"
SENSOR_SHORT_CIRCUIT_DETECTED = "Sensor short circuit detected"

# Strategy for detecting sensor issues (open and short circuits)
class SensorDetectionStrategy(ValidationStrategy):
    """
    This strategy checks if the ADC value is outside the valid range, which indicates an issue with the sensor:
    - If the ADC value is less than the open circuit threshold (LOW_THRESHOLD), it indicates that no sensor is detected (open circuit).
    - If the ADC value is greater than the safety threshold (HIGH_THRESHOLD), it indicates a potential short circuit.

    Validation:
    - The method ensures that the sensor is functioning properly by checking if the ADC value is within the valid range.
    """
    def validate(self, adc_value: int) -> Response:
        if adc_value < LOW_THRESHOLD:
            return Response(status=Status.EXCEPTION, details=NO_SENSOR_DETECTED, value=None)
        if adc_value > HIGH_THRESHOLD:
            return Response(status=Status.EXCEPTION, details=SENSOR_SHORT_CIRCUIT_DETECTED, value=None)
        return Response(status=Status.OK, details="Sensor detection successful", value=adc_value)


# Strategy for converting ADC value to current (mA)
class ADCToCurrentConversionStrategy(ValidationStrategy):
    """
    Converts the raw ADC value into the corresponding current in mA, considering the 200-ohm resistor.

    Includes tolerance check:
    - If the ADC value is between LOW_VALUE and LOW_THRESHOLD, it is considered 4mA.
    - If the ADC value is between HIGH_VALUE and HIGH_THRESHOLD, it is considered 20mA.

    return is rounded to avoid floating point issues
    """
    def validate(self, adc_value: int) -> Response:
        try:
            # Allow for tolerance in ADC values to determine 4mA or 20mA
            if LOW_THRESHOLD <= adc_value <= LOW_VALUE:
                current_ma = MIN_CURRENT_MA
            elif HIGH_VALUE <= adc_value <= HIGH_THRESHOLD:
                current_ma = MAX_CURRENT_MA
            else:
                # Convert ADC value to voltage (assuming a 4.096V reference)
                voltage = (adc_value / (ADC_RESOLUTION - ADC_OFF_SET)) * VOLTAGE_REF

                # Convert voltage to current (based on 200-ohm resistor)
                current_ma = (voltage / RESISTOR) * CONVERT_TO_MA  # Convert from A to mA

            return Response(status=Status.OK, details="ADC to current conversion successful", value=round(current_ma, 2))

        except Exception as e:
            return Response(status=Status.EXCEPTION, details=f"ADC to Current Conversion error: {e}", value=None)


# Strategy for converting current (mA) to temperature (Celsius)
class CurrentToTemperatureConversionStrategy(ValidationStrategy):
    """
    Converts the current (in mA) to temperature in Celsius.

    The sensor operates within a 4-20 mA range, and this strategy maps that range to a temperature range
    of 0°C to 50°C (or any other custom range provided).
    """
    def __init__(self, min_temp: LowTemperatureRange, max_temp: HighTemperatureRange):
        self.max_temp = max_temp.value
        self.min_temp = min_temp.value

    def validate(self, current_ma: float) -> Response:
        try:
            if not (MIN_CURRENT_MA <= current_ma <= MAX_CURRENT_MA):
                return Response(status=Status.EXCEPTION, details=f"Current {current_ma} is out of range", value=None)

            # Conversion formula: linear mapping from 4-20mA to the temperature range
            temperature_c = (((current_ma - MIN_CURRENT_MA) / (MAX_CURRENT_MA - MIN_CURRENT_MA))
                             * (self.max_temp - self.min_temp) + self.min_temp)

            return Response(status=Status.OK, details="Current to temperature conversion successful", value=temperature_c)
        except Exception as e:
            return Response(status=Status.EXCEPTION, details=f"Current to Temperature Conversion error: {e}", value=None)
