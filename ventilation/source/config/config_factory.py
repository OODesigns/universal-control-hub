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

    def create_loader(self, file_name):
        """
        Creates an instance of ConfigLoader for the given file name.

        :param file_name: The name of the config file (without directory path).
        :return: An instance of ConfigLoader initialized with the full file path.
        """
        full_path = os.path.join(self.directory, file_name)
        return ConfigLoader(full_path)

    def create_store(self, file_name):
        """
        Creates an instance of ConfigStore for the given file name.

        :param file_name: The name of the config file (without directory path).
        :return: An instance of ConfigStore initialized with the full file path.
        """
        full_path = os.path.join(self.directory, file_name)
        return ConfigStore(full_path)
