from typing import Type

from reader.device_reader import DeviceReader


class DeviceReaderSupplier:
    _client_class: Type[DeviceReader] = None

    @classmethod
    def register_client(cls, client_class: Type[DeviceReader]):
        """
        Registers a client class (a subclass of DeviceReader).
        """
        cls._client_class = client_class

    @classmethod
    def get(cls, device_to_read: str):
        """
        Instantiates the registered client class with the provided device_to_read parameter.
        """
        assert cls._client_class is not None, "The device reader class has not been assigned"
        return cls._client_class(device_to_read)
