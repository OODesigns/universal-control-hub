from blauberg.blauberg_mvhr import BlaubergMVHR
from devices.device_factory import DeviceFactory
from utils.standard_name import ssn

DeviceFactory.register_device(ssn("blauberg_mvhr"), BlaubergMVHR)


