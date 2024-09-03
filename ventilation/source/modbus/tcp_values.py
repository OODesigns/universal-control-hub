from re import compile

from utils.value import (ValidatedValue, ValidatedResponse, ValueStatus,
                         StrictValidatedValue, RangeValidatedValue)


class IPAddress(ValidatedValue):
    @classmethod
    def validate(cls, ip_address: str) -> ValidatedResponse:
        # Improved regex for IP address validation, including edge cases
        pattern = compile(
            r"^(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\."
            r"(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\."
            r"(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\."
            r"(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])$"
        )
        if not pattern.match(ip_address):
            return ValidatedResponse(
                status=ValueStatus.EXCEPTION,
                details=f"Invalid IP address: {ip_address}",
                value=None
            )
        return ValidatedResponse(
            status=ValueStatus.OK,
            details="",
            value=ip_address
        )


class StrictIPAddress(StrictValidatedValue, IPAddress):
    pass


class Port(RangeValidatedValue):
    valid_types = (int,)
    low_value = 0
    high_value = 65535


class StrictPort(StrictValidatedValue, Port):
    pass
