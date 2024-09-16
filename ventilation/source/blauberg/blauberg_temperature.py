from dataclasses import dataclass
from typing import List

from blauberg.blauberg_registers import InputRegisters
from utils.strategies import ExceptionCascade
from utils.temperaturecelsius import TemperatureCelsius
from utils.value import Response, ValidationStrategy
from utils.status import Status

SHORT_CIRCUIT = "Sensor short circuit"
NO_SENSOR = "No sensor detected"

CONVERSION_FACTOR = 10.0
NO_SENSOR_DETECTED = -32768
SENSOR_SHORT_CIRCUIT = 32767


class SensorDetection(ValidationStrategy):
    """
    A custom validation strategy to handle specific sensor cases:
    - No sensor detected
    - Sensor short circuit
    """
    @classmethod
    def validate(cls, value: int) -> Response:
        # Type check
        if not isinstance(value, int):
            return Response(status=Status.EXCEPTION, details="Invalid value type", value=None)

        # Check for specific sensor conditions
        if value == NO_SENSOR_DETECTED:
            return Response(status=Status.EXCEPTION, details=NO_SENSOR, value=None)
        if value == SENSOR_SHORT_CIRCUIT:
            return Response(status=Status.EXCEPTION, details=SHORT_CIRCUIT, value=None)

        # If no issues, return OK response
        return Response(status=Status.OK, details="Sensor check passed", value=value)


class RawDataToCelsiusConversion(ValidationStrategy):
    """
    A strategy to convert raw Modbus values to Celsius.
    """
    @classmethod
    def validate(cls, value: int) -> Response:
        try:
            celsius_value = value / CONVERSION_FACTOR
            return Response(status=Status.OK, details="Converted to Celsius", value=celsius_value)
        except ZeroDivisionError:
            return Response(status=Status.EXCEPTION, details="Conversion factor is zero", value=None)
        except TypeError:
            return Response(status=Status.EXCEPTION, details="Invalid input type", value=None)
        except Exception as e:
            return Response(status=Status.EXCEPTION, details=f"Unexpected error: {str(e)}", value=None)

class AllowedInputRegister(ValidationStrategy):
    """
    A custom validation strategy to check if the selected temperature register is valid
    based on the input register values.
    """
    # Class-level variable to store valid registers
    valid_registers = {
        InputRegisters.IR_CUR_SEL_TEMP.value,
        InputRegisters.IR_CURTEMP_SUAIR_IN.value,
        InputRegisters.IR_CURTEMP_SUAIR_OUT.value,
        InputRegisters.IR_CURTEMP_EXAIR_IN.value,
        InputRegisters.IR_CURTEMP_EXAIR_OUT.value,
        InputRegisters.IR_CURTEMP_EXT.value,
        InputRegisters.IR_CURTEMP_WATER.value,
    }

    def validate(self, selected_temp: int) -> Response:
        # Ensure the selected temperature is an integer
        if not isinstance(selected_temp, int):
            return Response(status=Status.EXCEPTION, details="Invalid value type", value=None)

        # Validate if the selected temperature register is in the valid set
        if selected_temp in self.valid_registers:
            return Response(status=Status.OK, details="Validation successful", value=selected_temp)
        else:
            return Response(status=Status.EXCEPTION, details="Invalid temperature selection", value=None)


@dataclass(frozen=True)
class InputRegistersStrategy(ValidationStrategy):
    input_register: Response[List[int]]

    def validate(self, value) -> Response:
        # Check if the register index is within the data_array bounds
        if value >= len(self.input_register.value) or value < 0:
            return Response(
                status=Status.EXCEPTION,
                details="Register selection out of bounds of input register",
                value=None
            )

        # Return the value from the data array
        register_value = self.input_register.value[value]
        return Response(
            status=Status.OK,
            details="Valid register and data found",
            value=register_value
        )


class BlaubergTemperature(TemperatureCelsius):

    def get__strategies(self) -> List[ValidationStrategy]:
        return [self._input_register_exception_cascade,
                AllowedInputRegister(),
                self._input_registers_strategy,
                SensorDetection(),
                RawDataToCelsiusConversion()] + super().get__strategies()

    def __init__(self, input_register: Response[List[int]], selected_temp: int):
        self._input_register_exception_cascade = ExceptionCascade(input_register)
        self._input_registers_strategy = InputRegistersStrategy(input_register)

        super().__init__(selected_temp)
