from utils.response import Response
from utils.status import Status
from utils.value import ValidationStrategy

# Constants for 4-20mA to temperature conversion with a 240-ohm resistor
MIN_CURRENT_MA = 4.0
MAX_CURRENT_MA = 20.0
VOLTAGE_REF = 5.0
ADC_RESOLUTION = 4096  # 12-bit ADC (MCP3208)
SAFETY_MARGIN_ADC = 3932  # ADC value at 4.8V with 240-ohm resistor for short-circuit detection
OPEN_CIRCUIT_THRESHOLD = 819  # ADC value at 0.96V for a 240-ohm resistor (4mA)
ADC_OFF_SET = 1
CONVERT_TO_MA = 1000.0
RESISTOR = 240.0

# Error messages
NO_SENSOR_DETECTED = "No sensor detected"
SENSOR_SHORT_CIRCUIT_DETECTED = "Sensor short circuit detected"

# Strategy for detecting sensor issues (open and short circuits)
class SensorDetection(ValidationStrategy):
    """
    This strategy checks if the ADC value is outside the valid range, which indicates an issue with the sensor:
    - If the ADC value is less than the open circuit threshold (819), it indicates that no sensor is detected (open circuit).
    - If the ADC value is greater than the safety threshold (3932), it indicates a potential short circuit.

    Validation:
    - The method ensures that the sensor is functioning properly by checking if the ADC value is within the valid range.
    """
    def validate(self, adc_value: int) -> Response:
        if adc_value < OPEN_CIRCUIT_THRESHOLD:
            return Response(status=Status.EXCEPTION, details=NO_SENSOR_DETECTED, value=None)
        if adc_value >= SAFETY_MARGIN_ADC:
            return Response(status=Status.EXCEPTION, details=SENSOR_SHORT_CIRCUIT_DETECTED, value=None)
        return Response(status=Status.OK, details="Sensor detection successful", value=adc_value)


# Strategy for converting ADC value to current (mA)
class ADCToCurrentConversionStrategy(ValidationStrategy):
    """
    Converts the raw ADC value into the corresponding current in mA, considering the 240-ohm resistor.

    """
    def validate(self, adc_value: int) -> Response:
        try:
            # Convert ADC value to voltage (assuming a 5V reference)
            voltage = (adc_value / (ADC_RESOLUTION - ADC_OFF_SET)) * VOLTAGE_REF

            # Convert voltage to current (based on 240-ohm resistor)
            current_ma = (voltage / RESISTOR) * CONVERT_TO_MA  # Convert from A to mA

            return Response(status=Status.OK, details="ADC to current conversion successful", value=current_ma)

        except Exception as e:
            return Response(status=Status.EXCEPTION, details=f"ADC to Current Conversion error: {e}", value=None)


# Strategy for converting current (mA) to temperature (Celsius)
class CurrentToTemperatureConversionStrategy(ValidationStrategy):
    """
    Converts the current (in mA) to temperature in Celsius.

    The sensor operates within a 4-20 mA range, and this strategy maps that range to a temperature range
    of 0°C to 50°C (or any other custom range provided).
    """
    def __init__(self, min_temp: int, max_temp: int):
        self.max_temp = max_temp
        self.min_temp = min_temp

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


# Strategy for validating the temperature range
class RestrictedRangeValidationStrategy(ValidationStrategy):
    """
    Ensures that the calculated temperature is within the valid range for the sensor.
    """
    def __init__(self, min_temp: int, max_temp: int):
        self.max_temp = max_temp
        self.min_temp = min_temp

    def validate(self, temperature_c: float) -> Response:
        if self.min_temp <= temperature_c <= self.max_temp:
            return Response(status=Status.OK, details="Temperature validation successful", value=temperature_c)
        return Response(status=Status.EXCEPTION, details=f"Temperature {temperature_c} out of range", value=None)