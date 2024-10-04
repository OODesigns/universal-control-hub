from dataclasses import dataclass

from spi.spi_client import SPIClient
from spi.spi_command import SPICommand
from utils.response import Response


@dataclass(frozen=True)
class MCP3208(SPIClient):

    def __init__(self, builder):
        pass

    def execute(self, command: SPICommand = None) -> Response:
        pass