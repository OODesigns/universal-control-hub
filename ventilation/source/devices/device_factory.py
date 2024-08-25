import importlib
import sys
from config.config_factory import ConfigFactory
from devices.device import Device
from state.state_manager import StateManager

DEVICES = "devices"

class DeviceFactory:
    _registry = {}
    _dependency = {}

    def __init__(self, config_factory: ConfigFactory, state_manager:StateManager):
        self._state_manager = state_manager
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

    # TODO Add Exception Handling when device does not load
    def create_device(self, device_name) ->Device:
        """Factory method to create a device instance."""
        if device_name not in DeviceFactory._registry:
            raise ValueError(f"Device '{device_name}' is not registered.")
        device_class = DeviceFactory._registry[device_name]

        # Prepare dependencies based on the device's required_dependencies
        dependencies = {}
        for dep_name in device_class.required_dependencies:
            if dep_name in DeviceFactory._dependency:
                dependencies[dep_name] = DeviceFactory._dependency[dep_name]()
            else:
                raise ValueError(f"Dependency '{dep_name}' is required by {device_name} but not provided.")

        # Create the device with the injected dependencies
        return device_class(self._config_factory.create_loader(device_name), self._state_manager, **dependencies)


    @classmethod
    def _load_registered_devices(cls):
        """Load the registered devices by importing the devices module."""
        if not cls._registry:
            importlib.import_module(DEVICES) # pragma: no cover

    @classmethod
    def _registered_devices_loaded(cls):
        """Check if the devices module is already loaded in sys.modules."""
        return DEVICES in sys.modules # pragma: no cover