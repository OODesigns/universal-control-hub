from blauberg.blauberg_mvhr import BlaubergMVHR
from devices.device_factory import DeviceFactory
from utils.standard_name import sn

DeviceFactory.register_device(sn("blauberg_mvhr"), BlaubergMVHR)


