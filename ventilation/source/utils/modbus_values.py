from utils.value import Value


class Retries(Value):
    def __init__(self, retries):
        super().__init__(self.validate(retries))

    @classmethod
    def validate(cls, retries):
        if not isinstance(retries, int) or not (0 <= retries <= 10):
            raise ValueError(f"Retries must be an integer between 0 and 10, got {retries}")
        return retries


class ReconnectDelay(Value):
    def __init__(self, delay):
        super().__init__(self.validate(delay))

    @classmethod
    def validate(cls, delay):
        if not isinstance(delay, (int, float)) or not (0.1 <= delay <= 300):
            raise ValueError(f"Reconnect delay must be a float or integer between 0.1 and 300 seconds, got {delay}")
        return delay


class ReconnectDelayMax(Value):
    def __init__(self, delay_max):
        super().__init__(self.validate(delay_max))

    @classmethod
    def validate(cls, delay_max):
        if not isinstance(delay_max, (int, float)) or not (0.1 <= delay_max <= 300):
            raise ValueError(
                f"Reconnect delay max must be a float or integer between 0.1 and 300 seconds, got {delay_max}")
        return delay_max


class Timeout(Value):
    def __init__(self, timeout):
        super().__init__(self.validate(timeout))

    @classmethod
    def validate(cls, timeout):
        if not isinstance(timeout, (int, float)) or not (0.1 <= timeout <= 60):
            raise ValueError(f"Timeout must be a float or integer between 0.1 and 60 seconds, got {timeout}")
        return timeout


class ModbusSize(Value):
    def __init__(self, size):
        super().__init__(self.validate(size))
        self._value = self.validate(size)

    @classmethod
    def validate(cls, size):
        if not isinstance(size, int) or not (0 <= size <= 65535):
            raise ValueError(f"{cls.__name__} must be an integer between 0 and 65535, got {size}")
        return size


class CoilSize(ModbusSize):
    pass


class DiscreteInputSize(ModbusSize):
    pass


class InputRegisterSize(ModbusSize):
    pass


class HoldingRegisterSize(ModbusSize):
    pass
