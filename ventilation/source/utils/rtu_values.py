from utils.value import Value


class BaudRate(Value):
    VALID_RATES = [9600, 14400, 19200, 38400, 57600, 115200]

    def __init__(self, baud_rate):
        super().__init__()
        self._value = self.validate(baud_rate)

    @classmethod
    def validate(cls, baud_rate):
        if baud_rate not in BaudRate.VALID_RATES:
            raise ValueError(f"Invalid baud rate: {baud_rate}. Must be one of {BaudRate.VALID_RATES}")
        return baud_rate

class StopBits(Value):
    VALID_BITS = [1, 1.5, 2]

    def __init__(self, stop_bits):
        super().__init__()
        self._value = self.validate(stop_bits)

    @classmethod
    def validate(cls,stop_bits):
        if stop_bits not in StopBits.VALID_BITS:
            raise ValueError(f"Invalid stop bits: {stop_bits}. Must be one of {StopBits.VALID_BITS}")
        return stop_bits