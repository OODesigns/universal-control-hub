from devices.device_factory import DeviceFactory
from reader.device_reader import DeviceReader
from utils.standard_name import sn, StandardName

ADC = "mpc3208"

class MPC3208DeviceReader(DeviceReader):
    ADC = None

    def get_device_name(self) -> str:
        return ADC

    def __init__(self, device_to_read: StandardName):
        super().__init__(device_to_read)
        self.mpc_3208: DeviceReader = DeviceFactory.get_device(sn(ADC), self.get_config_name()).device

    def read(self) -> int:
        return self.mpc_3208.read()

