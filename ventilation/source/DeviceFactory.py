from store import Store


class DeviceFactory:
    _registry = {}

    def __init__(self, store: Store):
        self._store = store

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
        return device_class(self._store)

