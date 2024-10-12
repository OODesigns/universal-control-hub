from typing import Type

from reader.device_reader import DeviceReader


class DeviceReaderSupplier:
    _client_class: Type[DeviceReader] = None

    @classmethod
    def register_client(cls, client_class: Type[DeviceReader]):
        """
        :type client_class: object
        """
        cls._client_class = client_class
