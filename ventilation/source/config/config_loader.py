import json
import os
from typing import Any


class ConfigLoader:
    def __init__(self, file_name):
        """
        Initializes the ConfigLoader with the given file name.
        This class is intended for read-only access to configuration data.
        """
        self._file_name = file_name
        self._data = {}
        self._ensure_file_exists()
        self._read_store()

    @classmethod
    def write_json(cls, data: dict, file: Any) -> None:
        json.dump(data, file)

    def _ensure_file_exists(self):
        """Ensures that the JSON fil`e exists. If not, creates an empty file."""
        if not os.path.exists(self._file_name):
            with open(self._file_name, 'w', encoding='utf-8') as f:
                ConfigLoader.write_json({}, f) # avoids typing warning


    def _read_store(self):
        """Loads the content of the store into the `self._data` dictionary."""
        with open(self._file_name, 'r') as f:
            self._data = json.load(f)

    def get_value(self, key):
        """
        Gets the value for a given key from the store.

        :param key: The key whose value is to be retrieved.
        :return: The value associated with the key, or None if the key does not exist.
        """
        return self._data.get(key)

    def get_array(self, key):
        """
        Gets an array of values associated with the given key.

        :param key: The key whose value is to be retrieved.
        :return: An array of values associated with the key, or an empty list if the key does not exist or is not an array.
        """
        value = self._data.get(key)
        if isinstance(value, list):
            return value
        return []
