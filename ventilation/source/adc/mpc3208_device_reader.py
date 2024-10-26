from devices.device_factory import DeviceFactory, DeviceResponse
from reader.device_reader import DeviceReader
from reader.reader import Reader
from utils.response import Response
from utils.standard_name import StandardName, ssn
from utils.status import Status

ADC = "mpc3208"

class MPC3208DeviceReader(DeviceReader[int]):
    def __init__(self, device_to_read: StandardName):
        super().__init__(device_to_read)
        device_to_read: DeviceResponse[Reader[int]] =  DeviceFactory.get_device(ssn(ADC), self.get_config_name())
        if device_to_read.status is Status.EXCEPTION:
            raise ValueError(device_to_read.details)

        self.mpc_3208: Reader[int] = device_to_read.device

    def get_device_name(self) -> str:
        return ADC

    def read(self) -> Response[int]:
        return self.mpc_3208.read()

