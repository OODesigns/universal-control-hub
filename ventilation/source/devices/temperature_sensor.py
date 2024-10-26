from config.config_loader import ConfigLoader
from devices.device import Device
from reader.device_reader import DeviceReader
from reader.device_reader_supplier import DeviceReaderSupplier
from utils.temperaturecelsius import TemperatureInterface

class TemperatureSensor(Device):
    def __init__(self, config_loader: ConfigLoader):
        super().__init__(config_loader)
        self.reader: DeviceReader[int] = DeviceReaderSupplier.get(config_loader)


    def get_temperature(self) -> TemperatureInterface:
        # self.mpc_3208: MCP3208 = DeviceFactory.get_device("mpc3208", "mcp3208_"+device_to_reed).device
        pass
