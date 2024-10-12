from adc.mcp3208 import MCP3208
from devices.device_factory import DeviceFactory

DeviceFactory.register_device("mcp3208", MCP3208)
