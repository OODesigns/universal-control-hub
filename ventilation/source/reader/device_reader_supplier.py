from typing import Type

from reader.device_reader import DeviceReader


class DeviceReaderSupplier:
    _reader_class: Type[DeviceReader] = None

    @classmethod
    def register_reader(cls, reader_class: Type[DeviceReader]):
        """
        Registers a reader class (a subclass of DeviceReader).
        """
        cls._reader_class = reader_class

    @classmethod
    def get(cls, device_to_read: str):
        """
        Instantiates the registered reader class with the provided device_to_read parameter.
        """
        assert cls._reader_class is not None, "The device reader class has not been assigned"
        return cls._reader_class(device_to_read)
