from ventilation.source.abstract_value import AbstractValue


class Temperature(AbstractValue):
    def __init__(self, value: int):
        super().__init__()
        if not (0 <= value <= 50):
            raise ValueError("Temperature must be between 0 and 50°C.")
        self._value = value


