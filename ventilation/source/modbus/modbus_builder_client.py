from abc import ABC, abstractmethod

from modbus.modbus import ModbusInterface


class ModbusBuilderClient(ModbusInterface, ABC):
    @abstractmethod
    def __init__(self, builder):
        pass
