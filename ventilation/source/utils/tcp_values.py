from re import compile

from utils.value import Value


class IPAddress(Value):
    def __init__(self, ip_address):
        super().__init__(self.validate(ip_address))

    @classmethod
    def validate(cls, ip_address):
        # Improved regex for IP address validation, including edge cases
        pattern = compile(
            r"^(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\."
            r"(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\."
            r"(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\."
            r"(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])$"
        )
        if not pattern.match(ip_address):
            raise ValueError(f"Invalid IP address: {ip_address}")
        return ip_address


class Port(Value):
    def __init__(self, port):
        super().__init__(self.validate(port))

    @classmethod
    def validate(cls, port):
        if not (0 <= port <= 65535):
            raise ValueError(f"Port number must be between 0 and 65535, got {port}")
        return port
