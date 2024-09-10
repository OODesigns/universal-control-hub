from abc import abstractmethod
from config.config_loader import ConfigLoader
from devices.device import Device
from mvhr_state import MVHRStateInterface
from utils.operation_response import OperationResponse


class MVHR(Device):
    def __init__(self, config_loader: ConfigLoader):
        super().__init__(config_loader)

    @abstractmethod
    async def read(self)-> MVHRStateInterface:  # pragma: no cover
        pass

    @abstractmethod
    async def start(self) -> OperationResponse: # pragma: no cover
        pass

    @abstractmethod
    def stop(self) -> OperationResponse: # pragma: no cover
        pass