import platform
import re
from enum import Enum

from utils.value import ValidatedValue, StrictValidatedValue, ValidatedResponse, ValueStatus

class ParityType(Enum):
    NONE = 'N'
    EVEN = 'E'
    ODD = 'O'

class SerialPort(ValidatedValue):
    @classmethod
    def validate(cls, port_name: str) -> ValidatedResponse:
        system = platform.system()

        if system == "Windows":
            pattern = r"^COM[1-9][0-9]*$"
            if not re.fullmatch(pattern, port_name):
                return ValidatedResponse(
                    status=ValueStatus.EXCEPTION,
                    details=f"Invalid serial port: {port_name}. Valid ports are COM1, COM2, ..., COMn",
                    value=None
                )

        elif system in ["Linux", "Darwin"]:
            pattern = r"^/dev/tty(S|USB)[1-9][0-9]*$|^/dev/tty(S|USB)0$"
            if not re.fullmatch(pattern, port_name):
                return ValidatedResponse(
                    status=ValueStatus.EXCEPTION,
                    details=f"Invalid serial port: {port_name}. Valid ports are /dev/ttyS0, /dev/ttyUSB0, ..., /dev/ttySn",
                    value=None
                )

        else:
            return ValidatedResponse(
                status=ValueStatus.EXCEPTION,
                details=f"Unsupported operating system: {system}",
                value=None
            )

        return ValidatedResponse(
            status=ValueStatus.OK,
            details="",
            value=port_name
        )

class StrictSerialPort(StrictValidatedValue, SerialPort):
    pass


class BaudRate(ValidatedValue):
    VALID_RATES = [9600, 14400, 19200, 38400, 57600, 115200]

    @classmethod
    def validate(cls, baud_rate: int) -> ValidatedResponse:
        if baud_rate not in BaudRate.VALID_RATES:
            return ValidatedResponse(
                status=ValueStatus.EXCEPTION,
                details=f"Invalid baud rate: {baud_rate}. Must be one of {BaudRate.VALID_RATES}",
                value=None
            )
        return ValidatedResponse(
            status=ValueStatus.OK,
            details="",
            value=baud_rate
        )

class StrictBaudRate(StrictValidatedValue, BaudRate):
    pass


class StopBits(ValidatedValue):
    VALID_BITS = [1, 1.5, 2]

    @classmethod
    def validate(cls, stop_bits: float) -> ValidatedResponse:
        if stop_bits not in StopBits.VALID_BITS:
            return ValidatedResponse(
                status=ValueStatus.EXCEPTION,
                details=f"Invalid stop bits: {stop_bits}. Must be one of {StopBits.VALID_BITS}",
                value=None
            )
        return ValidatedResponse(
            status=ValueStatus.OK,
            details="",
            value=stop_bits
        )

class StrictStopBits(StrictValidatedValue, StopBits):
    pass
