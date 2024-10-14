from adc.mcp3208 import MCP3208
from devices.device_factory import DeviceFactory
from utils.standard_name import sn

DeviceFactory.register_device(sn("mcp3208"), MCP3208)
