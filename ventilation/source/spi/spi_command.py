class SPICommand:
    def __init__(self, command: list, data: list = None):
        """
        SPICommand represents a command and optional data for SPI communication.
        :param command: List of byte values (integers between 0 and 255) that form the SPI command.
        :param data: Optional list of byte values (integers between 0 and 255) representing data to write.
        """
        if not all(isinstance(byte, int) and 0 <= byte <= 255 for byte in command):
            raise ValueError("Command must be a list of byte values (0-255).")
        self.command = command
        self.data = data or []

    def full_command(self) -> list:
        """Return the full command including any additional data."""
        return self.command + self.data

    def __str__(self):
        return f"SPICommand(command={self.command}, data={self.data})"
