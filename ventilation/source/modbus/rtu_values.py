import platform
import re
from enum import Enum

from utils.constants import DEFAULT_SUCCESS_MESSAGE
from utils.value import ValidatedValue, StrictValidatedValue, TypeValidationStrategy, EnumValidationStrategy
from utils.response import Response
from utils.status import Status


class ParityType(Enum):
    NONE = 'N'
    EVEN = 'E'
    ODD = 'O'


class SerialPort(ValidatedValue[str]):
    """
    A class that represents and validates a serial port name depending on the operating system.
    """

    def get__strategies(self):
        # Include TypeValidationStrategy to ensure the input is a string
        return [TypeValidationStrategy(str), SerialPortValidationStrategy()]

    def __init__(self, value: str):
        # Run validations and store value and validation status
        super().__init__(value)


class SerialPortValidationStrategy:
    """
    A custom validation strategy to check if the serial port name is valid depending on the operating system.
    """
    @classmethod
    def validate(cls, value: str) -> Response:
        system = platform.system()

        if system == "Windows":
            pattern = r"^COM[1-9][0-9]*$"
            if not re.fullmatch(pattern, value):
                return Response(
                    status=Status.EXCEPTION,
                    details=f"Invalid serial port: {value}. Valid ports are COM1, COM2, ..., COMn",
                    value=None
                )

        elif system in ["Linux", "Darwin"]:
            pattern = r"^/dev/tty(S|USB)[1-9][0-9]*$|^/dev/tty(S|USB)0$"
            if not re.fullmatch(pattern, value):
                return Response(
                    status=Status.EXCEPTION,
                    details=f"Invalid serial port: {value}. Valid ports are /dev/ttyS0, /dev/ttyUSB0, ..., /dev/ttySn",
                    value=None
                )

        else:
            return Response(
                status=Status.EXCEPTION,
                details=f"Unsupported operating system: {system}",
                value=None
            )

        return Response(status=Status.OK, details=DEFAULT_SUCCESS_MESSAGE, value=value)


class BaudRate(ValidatedValue[int]):
    """
    A class that represents and validates a baud rate from a predefined set of valid rates.
    """
    VALID_RATES = [9600, 14400, 19200, 38400, 57600, 115200]

    def get__strategies(self):
        # Include TypeValidationStrategy to ensure the input is an integer
        return [TypeValidationStrategy(int), EnumValidationStrategy(BaudRate.VALID_RATES)]

    def __init__(self, value: int):
        # Run validations and store value and validation status
        super().__init__(value)


class StopBits(ValidatedValue[int]):
    """
    A class that represents and validates stop bits for a serial connection.

    stop bits are used to signal the end of a data packet or byte being transmitted.
    They provide a break or idle period between consecutive bytes to allow the receiver to
    recognize the boundaries between bytes and to prepare for the next byte.

    1.5 Stop Bits: This is used in rare configurations, decided to see if we can use int values

    """
    VALID_BITS = [1, 2]

    def get__strategies(self):
        # Include TypeValidationStrategy to ensure the input is an integer
        return [TypeValidationStrategy(int), EnumValidationStrategy(StopBits.VALID_BITS)]

    def __init__(self, value: int):
        # Run validations and store value and validation status
        super().__init__(value)


# Strict versions that automatically raise exceptions if validation fails
class StrictSerialPort(SerialPort, StrictValidatedValue):
    pass


class StrictBaudRate(BaudRate, StrictValidatedValue):
    pass


class StrictStopBits(StopBits, StrictValidatedValue):
    pass
