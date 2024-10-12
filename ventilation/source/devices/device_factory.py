import importlib
import pkgutil
import sys
from dataclasses import dataclass
from enum import Enum
from config.config_factory import ConfigFactory
from devices.device import Device
from typing import Optional, TypeVar, Generic

REGISTERED = "registered"


class DeviceStatus(Enum):
    VALID = 0
    EXCEPTION = 1


T = TypeVar('T', bound=Device)


@dataclass
class DeviceResponse(Generic[T]):
    status: DeviceStatus
    details: str
    device: Optional[T]


class DeviceFactory:
    _instance = None
    _registry = {}
    _dependency = {}

    @classmethod
    def get_device(cls, device_name: str, config_name: str = None) -> DeviceResponse[T]:
        if DeviceFactory._instance is None:
            return DeviceResponse(
                status=DeviceStatus.EXCEPTION,
                details=f"Device factory is not initialized.",
                device=None
            )
        return DeviceFactory._instance.create(device_name, config_name)

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config_factory: ConfigFactory):
        self._config_factory = config_factory
        if not self._registered_devices_loaded():
            self._load_registered_devices()

    @classmethod
    def register_device(cls, name, device_class):
        if issubclass(device_class, Device) and name not in cls._registry:
            cls._registry[name] = device_class

    @classmethod
    def register_dependency(cls, name, dependency_class: any):
        if name not in cls._dependency:
            cls._dependency[name] = dependency_class

    def create(self, device_name: str, config_name: str = None) -> DeviceResponse[T]:
        """Factory method to create a device instance."""
        if device_name not in DeviceFactory._registry:
            return DeviceResponse(
                status=DeviceStatus.EXCEPTION,
                details=f"Device '{device_name}' is not registered.",
                device=None
            )
        device_class = DeviceFactory._registry[device_name]
        config_loader = self._config_factory.create_loader(device_name if config_name is None else config_name)

        # Load dependencies from both the config and required_dependencies
        dependencies = {}

        # Load dependencies from the config_loader for this device
        config_dependencies = config_loader.get_array('dependencies')

        for dep_name in set(config_dependencies + device_class.required_dependencies):
            if dep_name in DeviceFactory._dependency:
                dependencies[dep_name] = DeviceFactory._dependency[dep_name]()
            else:
                return DeviceResponse(
                    status=DeviceStatus.EXCEPTION,
                    details=f"Dependency '{dep_name}' is required by {device_name} but not provided.",
                    device=None
                )

        # Create the device with the injected dependencies
        device = device_class(config_loader, **dependencies)
        return DeviceResponse(
            status=DeviceStatus.VALID,
            details=f"Device {device_name} has been initialized.",
            device=device
        )

    @classmethod
    def _load_registered_devices(cls):
        """Dynamically import all modules in the specified package."""
        try:
            package = importlib.import_module(REGISTERED)
        except ImportError as e:
            raise ImportError(f"Failed to import package '{REGISTERED}': {e}")

        for _, module_name, _ in pkgutil.iter_modules(package.__path__):
            try:
                importlib.import_module(f"{REGISTERED}.{module_name}")
            except ImportError as e:
                raise ImportError(f"Failed to import module '{module_name}' from '{REGISTERED}': {e}")

    @classmethod
    def _registered_devices_loaded(cls):
        """Check if the devices module is already loaded in sys.modules."""
        return REGISTERED in sys.modules
