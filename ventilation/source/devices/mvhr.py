from abc import abstractmethod
from config.config_loader import ConfigLoader
from devices.device import Device
from modbus.modbus import ModbusInterface
from modbus.modbus_factory import ModbusFactory
from mvhr_repository import MVHRRepositoryInterface
from utils.value import ValidatedResponse


class MVHR(Device):
    def __init__(self, config_loader: ConfigLoader, modbus_factory: ModbusFactory):
        super().__init__(config_loader)
        self._modbus_factory = modbus_factory

    @property
    @abstractmethod
    def modbus(self) -> ModbusInterface:  # pragma: no cover
        pass

    @abstractmethod
    async def read_data(self)-> MVHRRepositoryInterface:  # pragma: no cover
        pass

    async def start(self) -> ValidatedResponse:
        """
        Start the MVHR device connection process.
        """
        return await self.modbus.connect()

    def stop(self) -> ValidatedResponse:
        return self.modbus.disconnect()

