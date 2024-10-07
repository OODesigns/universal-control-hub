from utils.value import RangeValidatedValue, StrictValidatedValue


class Retries(RangeValidatedValue[int]):
    """
    A class that represents and validates the number of retries for Modbus communication.
    """

    def __init__(self, value: int):
        super().__init__(value, int, 0, 10)


class StrictRetries(StrictValidatedValue, Retries):
    pass


class ReconnectDelay(RangeValidatedValue[float]):
    """
    A class that represents and validates the reconnect delay in Modbus communication.
    """

    def __init__(self, value: float):
        super().__init__(value, (float, int), 0.1, 300)


class StrictReconnectDelay(StrictValidatedValue, ReconnectDelay):
    pass


class ReconnectDelayMax(RangeValidatedValue[float]):
    """
    A class that represents and validates the maximum reconnect delay in Modbus communication.
    """

    def __init__(self, value: float):
        super().__init__(value, (float, int), 0.1, 300)


class StrictReconnectDelayMax(StrictValidatedValue, ReconnectDelayMax):
    pass


class Timeout(RangeValidatedValue[float]):
    """
    A class that represents and validates the timeout in Modbus communication.
    """

    def __init__(self, value: float):
        super().__init__(value, (float, int), 0.1, 60)


class StrictTimeout(StrictValidatedValue, Timeout):
    pass


class ModbusSize(RangeValidatedValue[int]):
    """
    A class that represents and validates the size of Modbus data structures (e.g., coils, registers).
    """

    def __init__(self, value: int):
        super().__init__(value, int, 0, 65535)


class StrictModbusSize(StrictValidatedValue, ModbusSize):
    pass


class CoilSize(ModbusSize):
    pass


class StrictCoilSize(StrictModbusSize, CoilSize):
    pass


class DiscreteInputSize(ModbusSize):
    pass


class StrictDiscreteInputSize(StrictModbusSize, DiscreteInputSize):
    pass


class InputRegisterSize(ModbusSize):
    pass


class StrictInputRegisterSize(StrictModbusSize, InputRegisterSize):
    pass


class HoldingRegisterSize(ModbusSize):
    pass


class StrictHoldingRegisterSize(StrictModbusSize, HoldingRegisterSize):
    pass
