from typing import Type, Generic, Optional

from reader.device_reader import DeviceReader
from reader.reader import T
from utils.standard_name import StandardName

class DeviceReaderSupplier(Generic[T]):
    _reader_class: Optional[Type[DeviceReader[T]]] = None

    @classmethod
    def register_reader(cls, reader_class: Type[DeviceReader[T]]):
        """
        Registers a reader class (a subclass of DeviceReader).
        :param reader_class:

        """
        cls._reader_class = reader_class

    @classmethod
    def get(cls, device_to_read: StandardName) -> DeviceReader[T]:
        """
        Instantiates the registered reader class with the provided device_to_read parameter.
        """
        assert cls._reader_class is not None, "The device reader class has not been assigned"
        return cls._reader_class(device_to_read)
