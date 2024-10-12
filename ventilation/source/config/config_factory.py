import os

from config.config_loader import ConfigLoader
from config.config_store import ConfigStore


class ConfigFactory:
    def __init__(self, directory):
        """
        Initializes the ConfigFactory with a base directory.

        :param directory: The base directory where the config files are located.
        """
        self.directory = directory

    def _get_full_path(self, file_name):
        return os.path.join(self.directory, file_name)

    def create_loader(self, file_name) -> ConfigLoader:
        """
        Creates an instance of ConfigLoader for the given file name.

        :param file_name: The name of the config file (without directory path).
        :return: An instance of ConfigLoader initialized with the full file path.
        """
        return ConfigLoader(self._get_full_path(file_name))

    def create_store(self, file_name) -> ConfigStore:
        """
        Creates an instance of ConfigStore for the given file name.

        :param file_name: The name of the config file (without directory path).
        :return: An instance of ConfigStore initialized with the full file path.
        """
        return ConfigStore(self._get_full_path(file_name))
