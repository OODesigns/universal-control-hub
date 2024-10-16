from typing import List

from utils.response import Response
from utils.strategies import ExceptionCascadeStrategy
from utils.temperaturecelsius import TemperatureCelsius
from utils.value import ValidationStrategy


class SPITemperature(TemperatureCelsius):

    def get__strategies(self) -> List[ValidationStrategy]:
        return [self._spi_exception_cascade] + super().get__strategies()

    def __init__(self, spi_response: Response[int]):
        self._spi_exception_cascade = ExceptionCascadeStrategy(spi_response)

        super().__init__(spi_response.value)
