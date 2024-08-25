from utils.value import RangeValidatedValue, StrictValidatedValue

class Retries(RangeValidatedValue):
    valid_types = (int,)
    low_value = 0
    high_value = 10

class StrictRetries(StrictValidatedValue, Retries):
    pass

class ReconnectDelay(RangeValidatedValue):
    valid_types = (int, float)
    low_value = 0.1
    high_value = 300

class StrictReconnectDelay(StrictValidatedValue, ReconnectDelay):
    pass

class ReconnectDelayMax(RangeValidatedValue):
    valid_types = (int, float)
    low_value = 0.1
    high_value = 300

class StrictReconnectDelayMax(StrictValidatedValue, ReconnectDelayMax):
    pass

class Timeout(RangeValidatedValue):
    valid_types = (int, float)
    low_value = 0.1
    high_value = 60

class StrictTimeout(StrictValidatedValue, Timeout):
    pass

class ModbusSize(RangeValidatedValue):
    valid_types = (int,)
    low_value = 0
    high_value = 65535

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
