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

class TemperatureValidationStrategy:
    """
    A custom validation strategy to handle specific sensor cases
    (no sensor detected, sensor short circuit) and convert raw Modbus values to Celsius.
    """
    @classmethod
    def validate(cls, value: int) -> Response:
        if value == NO_SENSOR_DETECTED:
            return Response(status=Status.EXCEPTION, details=NO_SENSOR, value=None)
        if value == SENSOR_SHORT_CIRCUIT:
            return Response(status=Status.EXCEPTION, details=SHORT_CIRCUIT, value=None)
        # Convert raw Modbus value to Celsius
        return Response(status=Status.OK, details="Validation successful", value=value / CONVERSION_FACTOR)

class RegisterValidationStrategy:
    """
    A custom validation strategy to check if the selected temperature register is valid
    based on the input register values.
    """

    def __init__(self, data_array: List[int]):
        super().__init__()
        self.data_array = data_array

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
            return Response(status=Status.OK, details="Validation successful", value= self.data_array[selected_temp])
        else:
            return Response(status=Status.EXCEPTION, details="Invalid temperature selection", value=None)

class BlaubergTemperature(TemperatureCelsius):

    def get__strategies(self) -> List[ValidationStrategy]:
        return [self._RegisterStrategy, TemperatureValidationStrategy()] + super().get__strategies()

    def __init__(self,  data_array: List[int], selected_temp: int):
        self._RegisterStrategy =  RegisterValidationStrategy(data_array)

        super().__init__(selected_temp)



