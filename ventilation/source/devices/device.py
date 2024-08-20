from abc import ABC

from config.config_loader import ConfigLoader
from state.state_manager import StateManager


class Device(ABC):
    required_dependencies = []

    def __init__(self, config_loader:ConfigLoader, state_manager:StateManager):
        self._name = None
        self._state_manager = state_manager
        self._config_loader = config_loader

