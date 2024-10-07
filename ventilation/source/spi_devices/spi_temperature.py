from typing import List

from utils.response import Response
from utils.strategies import ExceptionCascade
from utils.temperaturecelsius import TemperatureCelsius
from utils.value import ValidationStrategy


class SPITemperature(TemperatureCelsius):

    def get__strategies(self) -> List[ValidationStrategy]:
        return [self._spi_exception_cascade] + super().get__strategies()

    def __init__(self, spi_response: Response[int]):
        self._spi_exception_cascade = ExceptionCascade(spi_response)

        super().__init__(spi_response.value)
