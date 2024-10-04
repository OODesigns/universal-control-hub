from dataclasses import dataclass

from readers.device_reader import DeviceReader


@dataclass(frozen=True)
class MCP3208(DeviceReader):

    def read(self) -> int:
        pass

    def __init__(self):
        pass
