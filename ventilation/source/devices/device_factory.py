import importlib
import sys
from config.config_factory import ConfigFactory

DEVICES = "devices"

class DeviceFactory:
    _registry = {}
    def __init__(self, config_factory: ConfigFactory):
        self._config_factory = config_factory
        if not self._registered_devices_loaded():
            self._load_registered_devices()

    @classmethod
    def register_device(cls, device_name):
        """Decorator to register a device class with the factory."""
        def decorator(device_class):
            cls._registry[device_name] = device_class
            return device_class
        return decorator

    def create_device(self, device_name):
        """Factory method to create a device instance."""
        if device_name not in DeviceFactory._registry:
            raise ValueError(f"Device '{device_name}' is not registered.")
        device_class = DeviceFactory._registry[device_name]
        return device_class(self._config_factory.create_loader(device_name))

    @classmethod
    def _load_registered_devices(cls):
        """Load the registered devices by importing the devices module."""
        if not cls._registry:
            importlib.import_module(DEVICES) # pragma: no cover

    @classmethod
    def _registered_devices_loaded(cls):
        """Check if the devices module is already loaded in sys.modules."""
        return DEVICES in sys.modules # pragma: no cover