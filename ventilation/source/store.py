import json
import os

class Store:
    def __init__(self, file_name):
        """
        Initializes the Store with the given file name.

        :param file_name: The name of the JSON file to use for storing data.
        """
        self._file_name = file_name
        self._data = {}

    def _ensure_file_exists(self):
        """Ensures that the JSON file exists. If not, creates an empty file."""
        if not os.path.exists(self._file_name):
            with open(self._file_name, 'w') as f:
                json.dump({}, f)

    def _read_store(self):
        """Loads the content of the store into the `self.data` dictionary."""
        with open(self._file_name, 'r') as f:
            self._data = json.load(f)

    def _write_store(self):
        """Writes the `self.data` dictionary to the store and verifies the data was saved correctly."""
        # Save the current in-memory data to the file
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

    def get_value(self, key):
        """
        Gets the value for a given key from the store.

        :param key: The key whose value is to be retrieved.
        :return: The value associated with the key, or None if the key does not exist.
        """
        return self._data.get(key)
