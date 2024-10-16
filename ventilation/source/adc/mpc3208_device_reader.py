from devices.device_factory import DeviceFactory
from reader.device_reader import DeviceReader
from reader.reader import Reader
from utils.response import Response
from utils.standard_name import sn, StandardName

ADC = "mpc3208"

class MPC3208DeviceReader(DeviceReader[int]):
    def __init__(self, device_to_read: StandardName):
        super().__init__(device_to_read)
        self.mpc_3208: Reader[int] = DeviceFactory.get_device(sn(ADC), self.get_config_name()).device

    def get_device_name(self) -> str:
        return ADC

    def read(self) -> Response[int]:
        return self.mpc_3208.read()

