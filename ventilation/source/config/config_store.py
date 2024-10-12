import json

from config.config_loader import ConfigLoader


class ConfigStore(ConfigLoader):
    def __init__(self, file_name):
        """
        Initializes the ConfigStore with the given file name.
        This store allows both read and write operations.
        """
        super().__init__(file_name)

    def _write_store(self):
        """Writes the `self._data` dictionary to the store and verifies the data was saved correctly."""
        with open(self._file_name, 'w') as f:
            json.dump(self._data, f, indent=4)

        saved_data = self._data
        self._read_store()

        if self._data != saved_data:
            raise IOError("Failed to save data correctly to the store.")

    def set_value(self, key, value):
        """
        Sets the value for a given key in the store.

        :param key: The key under which the value is stored.
        :param value: The value to store.
        """
        self._data[key] = value
        self._write_store()
