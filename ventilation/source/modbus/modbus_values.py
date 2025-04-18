from utils.value import RangeValidatedValue, StrictValidatedValue


class Retries(RangeValidatedValue[int]):
    """
    A class that represents and validates the number of retries for Modbus communication.
    """

    def __init__(self, value: int):
        super().__init__(value, int, 0, 10)


class StrictRetries(Retries, StrictValidatedValue):
    pass


class ReconnectDelay(RangeValidatedValue[float]):
    """
    A class that represents and validates the reconnect delay in Modbus communication.
    """

    def __init__(self, value: float):
        super().__init__(value, (float, int), 0.1, 300)


class StrictReconnectDelay(ReconnectDelay, StrictValidatedValue):
    pass


class ReconnectDelayMax(RangeValidatedValue[float]):
    """
    A class that represents and validates the maximum reconnect delay in Modbus communication.
    """

    def __init__(self, value: float):
        super().__init__(value, (float, int), 0.1, 300)


class StrictReconnectDelayMax(ReconnectDelayMax, StrictValidatedValue):
    pass


class Timeout(RangeValidatedValue[float]):
    """
    A class that represents and validates the timeout in Modbus communication.
    """

    def __init__(self, value: float):
        super().__init__(value, (float, int), 0.1, 60)


class StrictTimeout(Timeout, StrictValidatedValue):
    pass


class ModbusSize(RangeValidatedValue[int]):
    """
    A class that represents and validates the size of Modbus data structures (e.g., coils, registers).
    """

    def __init__(self, value: int):
        super().__init__(value, int, 0, 65535)


class StrictModbusSize(ModbusSize, StrictValidatedValue):
    pass


class CoilSize(ModbusSize):
    pass


class StrictCoilSize(CoilSize, StrictModbusSize):
    pass


class DiscreteInputSize(ModbusSize):
    pass


class StrictDiscreteInputSize(DiscreteInputSize, StrictModbusSize):
    pass


class InputRegisterSize(ModbusSize):
    pass


class StrictInputRegisterSize(InputRegisterSize, StrictModbusSize):
    pass


class HoldingRegisterSize(ModbusSize):
    pass


class StrictHoldingRegisterSize(HoldingRegisterSize, StrictModbusSize):
    pass
