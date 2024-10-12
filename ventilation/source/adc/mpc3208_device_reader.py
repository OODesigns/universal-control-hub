from devices.device_factory import DeviceFactory
from reader.device_reader import DeviceReader


class MPC3208DeviceReader(DeviceReader):
    def __init__(self, device_to_reed: str):
        self.mpc_3208: DeviceReader = DeviceFactory.get_device("mpc3208", "mcp3208_"+device_to_reed).device

    def read(self) -> int:
        return self.mpc_3208.read()

