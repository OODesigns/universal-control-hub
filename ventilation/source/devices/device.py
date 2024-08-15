from abc import ABC

from config.config_loader import ConfigLoader


class Device(ABC):
    required_dependencies = []

    def __init__(self, config_loader:ConfigLoader):
        self._name = None
        self._config_loader = config_loader

