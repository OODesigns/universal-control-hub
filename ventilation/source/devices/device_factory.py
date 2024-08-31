import importlib
import sys
from dataclasses import dataclass
from enum import Enum

from config.config_factory import ConfigFactory
from devices.device import Device
from typing import Optional

DEVICES = "devices"

class DeviceStatus(Enum):
    VALID = 0
    EXCEPTION = 1

@dataclass
class DeviceResponse:
    status: DeviceStatus
    details: str
    device: Optional[Device]

class DeviceFactory:
    _registry = {}
    _dependency = {}

    def __init__(self, config_factory: ConfigFactory):
        self._config_factory = config_factory
        if not self._registered_devices_loaded():
            self._load_registered_devices()

    @classmethod
    def register_device(cls, name):
        """Decorator to register a device class with the factory."""
        def decorator(device_class):
            cls._registry[name] = device_class
            return device_class
        return decorator

    @classmethod
    def register_dependency(cls, name):
        """Decorator to register a dependencies class with the factory."""
        def decorator(dependency_class):
            cls._dependency[name] = dependency_class
            return dependency_class
        return decorator

    def create_device(self, device_name) -> DeviceResponse:
        """Factory method to create a device instance."""
        if device_name not in DeviceFactory._registry:
            return DeviceResponse(
                status=DeviceStatus.EXCEPTION,
                details=f"Device '{device_name}' is not registered.",
                device=None
            )
        device_class = DeviceFactory._registry[device_name]

        # Prepare dependencies based on the device's required_dependencies
        dependencies = {}
        for dep_name in device_class.required_dependencies:
            if dep_name in DeviceFactory._dependency:
                dependencies[dep_name] = DeviceFactory._dependency[dep_name]()
            else:
                return DeviceResponse(
                    status=DeviceStatus.EXCEPTION,
                    details=f"Dependency '{dep_name}' is required by {device_name} but not provided.",
                    device=None
                )

        # Create the device with the injected dependencies
        device = device_class(self._config_factory.create_loader(device_name), **dependencies)
        return DeviceResponse(
            status=DeviceStatus.VALID,
            details=f"Device {device_name} has been initialized.",
            device=device
        )

    @classmethod
    def _load_registered_devices(cls):
        """Load the registered devices by importing the devices module."""
        if not cls._registry:
            importlib.import_module(DEVICES)

    @classmethod
    def _registered_devices_loaded(cls):
        """Check if the devices module is already loaded in sys.modules."""
        return DEVICES in sys.modules
