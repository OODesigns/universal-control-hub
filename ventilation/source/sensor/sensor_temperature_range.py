from utils.value import RangeValidatedValue


class LowTemperatureRange(RangeValidatedValue[int]):
    """
    LowTemperatureRange represents the valid temperature range between -20°C and 0°C.
    """
    def __init__(self, value: int):
        super().__init__(value, int, -20, 0)

class HighTemperatureRange(RangeValidatedValue[int]):
    """
    HighTemperatureRange represents the valid temperature range between 40°C and 50°C.
    """
    def __init__(self, value: int):
        super().__init__(value, int, 40, 50)