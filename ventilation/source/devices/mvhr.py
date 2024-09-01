from abc import abstractmethod
from config.config_loader import ConfigLoader
from devices.device import Device
from mvhr_repository import MVHRRepositoryInterface
from utils.connection_reponse import ConnectionResponse

class MVHR(Device):
    def __init__(self, config_loader: ConfigLoader):
        super().__init__(config_loader)

    @abstractmethod
    async def read_data(self)-> MVHRRepositoryInterface:  # pragma: no cover
        pass

    @abstractmethod
    async def start(self) -> ConnectionResponse: # pragma: no cover
        pass

    @abstractmethod
    def stop(self) -> ConnectionResponse: # pragma: no cover
        pass

