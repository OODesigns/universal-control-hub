from re import compile
from utils.value import ValidatedValue, RangeValidatedValue, StrictValidatedValue, TypeValidationStrategy, \
    RangeValidationStrategy
from utils.response import Response
from utils.status import Status


class IPAddress(ValidatedValue[str]):
    """
    A class that represents and validates an IP address.
    """
    def get__strategies(self):
        # Include TypeValidationStrategy to ensure the input is a string
        return [
            TypeValidationStrategy(str),  # Ensure the value is a string
            IPAddressValidationStrategy()    # Validate the IP address format
        ]

    def __init__(self, value: str):
        # Run validations and store value and validation status
        super().__init__(value)


class IPAddressValidationStrategy:
    """
    A custom validation strategy to check if a value is a valid IP address.
    """
    @classmethod
    def validate(cls, value: str) -> Response:
        # Regex for IP address validation, including edge cases
        pattern = compile(
            r"^(25[0-5]|2[0-4][0-9]|1[0-9]{2}|1[0-9]{1}[0-9]|[1-9]?[0-9])\."
            r"(25[0-5]|2[0-4][0-9]|1[0-9]{2}|1[0-9]{1}[0-9]|[1-9]?[0-9])\."
            r"(25[0-5]|2[0-4][0-9]|1[0-9]{2}|1[0-9]{1}[0-9]|[1-9]?[0-9])\."
            r"(25[0-5]|2[0-4][0-9]|1[0-9]{2}|1[0-9]{1}[0-9]|[1-9]?[0-9])$"
        )
        if not pattern.match(value):
            return Response(
                status=Status.EXCEPTION,
                details=f"Invalid IP address: {value}",
                value=None
            )
        return Response(status=Status.OK, details="IP address is valid", value=value)


class Port(RangeValidatedValue[int]):
    """
    A class that represents and validates a TCP port number (0 to 65535).
    """
    def get__strategies(self):
        # Include TypeValidationStrategy to ensure the input is an integer
        return [
            TypeValidationStrategy(int),  # Ensure the value is an integer
            RangeValidationStrategy(0, 65535)  # Validate the port range
        ]

    def __init__(self, value: int):
        # Run validations and store value and validation status
        super().__init__(value, int, 0, 65535)


# Strict versions that automatically raise exceptions if validation fails
class StrictIPAddress(IPAddress, StrictValidatedValue):
    """
    A strict version of IPAddress that raises an exception if validation fails.
    """
    pass


class StrictPort(Port, StrictValidatedValue):
    """
    A strict version of Port that raises an exception if validation fails.
    """
    pass
