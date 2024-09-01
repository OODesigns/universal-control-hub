from utils.temperaturecelsius import TemperatureCelsius
from utils.value import ValidatedResponse, ValueStatus

SHORT_CIRCUIT = "Sensor short circuit"
NO_SENSOR = "No sensor detected"

CONVERSION_FACTOR = 10.0
NO_SENSOR_DETECTED = -32768
SENSOR_SHORT_CIRCUIT = 32767

class BlaubergTemperature(TemperatureCelsius):
    """
    A class that provides temperature validation and conversion based on the
    blauberg modbus table.
    """

    @classmethod
    def validate(cls, value) -> ValidatedResponse:
        if value in (NO_SENSOR_DETECTED, SENSOR_SHORT_CIRCUIT):
            return ValidatedResponse(
                status=ValueStatus.EXCEPTION,
                details=NO_SENSOR if value == NO_SENSOR_DETECTED else SHORT_CIRCUIT,
                value=None
            )

        # Convert raw Modbus value to Celsius and then validate
        celsius_value = value / CONVERSION_FACTOR

        # Use TemperatureCelsius validate method for validation
        return super().validate(celsius_value)
