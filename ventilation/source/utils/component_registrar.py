import importlib
import sys


class ComponentRegistrar:
    REGISTERED = "registered"

    @classmethod
    def load_registered_components(cls):
        """Dynamically import all modules in the specified package."""
        try:
            importlib.import_module(cls.REGISTERED)
        except ImportError as e:
            raise ImportError(f"Failed to import package '{cls.REGISTERED}': {e}")

    @classmethod
    def registered_components_loaded(cls):
        """Check if the components module is already loaded in sys.modules."""
        return cls.REGISTERED in sys.modules
