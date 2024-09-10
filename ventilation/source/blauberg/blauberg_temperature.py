from typing import List

from blauberg.blauberg_registers import InputRegisters
from utils.temperaturecelsius import TemperatureCelsius
from utils.value import Response, ValidationStrategy
from utils.status import Status

SHORT_CIRCUIT = "Sensor short circuit"
NO_SENSOR = "No sensor detected"

CONVERSION_FACTOR = 10.0
NO_SENSOR_DETECTED = -32768
SENSOR_SHORT_CIRCUIT = 32767


class CustomSensorStrategy(ValidationStrategy):
    """
    A custom validation strategy to handle specific sensor cases:
    - No sensor detected
    - Sensor short circuit
    """
    @classmethod
    def validate(cls, value: int) -> Response:
        if value == NO_SENSOR_DETECTED:
            return Response(status=Status.EXCEPTION, details=NO_SENSOR, value=None)
        if value == SENSOR_SHORT_CIRCUIT:
            return Response(status=Status.EXCEPTION, details=SHORT_CIRCUIT, value=None)
        # If no error, continue the chain
        return Response(status=Status.OK, details="Sensor check passed", value=value)

class ConversionStrategy(ValidationStrategy):
    """
    A strategy to convert raw Modbus values to Celsius.
    """
    @classmethod
    def validate(cls, value: int) -> Response:
        celsius_value = value / CONVERSION_FACTOR
        return Response(status=Status.OK, details="Converted to Celsius", value=celsius_value)


class RegisterEnumStrategy(ValidationStrategy):
    """
    A custom validation strategy to check if the selected temperature register is valid
    based on the input register values.
    """
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
        if selected_temp in self.valid_registers:
            return Response(status=Status.OK, details="Validation successful", value=selected_temp)
        else:
            return Response(status=Status.EXCEPTION, details="Invalid temperature selection", value=None)


class InputRegistersStrategy(ValidationStrategy):
    def __init__(self, data_array: List[int]):
        super().__init__()
        self.data_array = data_array

    def validate(self, value) -> Response:
        # Check if the register index is within the data_array bounds
        if value >= len(self.data_array) or value < 0:
            return Response(
                status=Status.EXCEPTION,
                details="Register index out of bounds in data array",
                value=None
            )

        # Return the value from the data array
        register_value = self.data_array[value]
        return Response(
            status=Status.OK,
            details="Valid register and data found",
            value=register_value
        )


class BlaubergTemperature(TemperatureCelsius):

    def get__strategies(self) -> List[ValidationStrategy]:
        return [RegisterEnumStrategy(), self._input_registers_strategy,
                CustomSensorStrategy(), ConversionStrategy()] + super().get__strategies()

    def __init__(self, data_array: List[int], selected_temp: int):
        self._input_registers_strategy = InputRegistersStrategy(data_array)

        super().__init__(selected_temp)
