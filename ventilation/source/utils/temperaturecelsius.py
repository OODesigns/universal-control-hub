from abc import ABC

from utils.value import ValidatedValue, ValueStatus, ValidatedResult, StrictValidatedValue


class TemperatureInterface(ValidatedValue, ABC):
    pass

class TemperatureCelsius(TemperatureInterface):
    @classmethod
    def validate(cls, validated_value: float):
        if not (-20 <= validated_value <= 50):
            return ValidatedResult(status=ValueStatus.EXCEPTION,
                                   details="Temperature must be between -20 and 50°C.",
                                   value=validated_value)

        return ValidatedResult(status=ValueStatus.OK, details="", value=validated_value)

class StrictTemperatureCelsius(StrictValidatedValue, TemperatureCelsius):
    pass