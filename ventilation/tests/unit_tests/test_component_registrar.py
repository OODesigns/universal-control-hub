import unittest
from unittest.mock import patch, MagicMock
import sys

from utils.component_registrar import ComponentRegistrar


class TestComponentRegistrar(unittest.TestCase):

    def setUp(self):
        # Clean up sys.modules before each test
        if ComponentRegistrar.REGISTERED in sys.modules:
            del sys.modules[ComponentRegistrar.REGISTERED]

    def test_load_registered_components_success(self):
        # Test successful import of registered package
        with patch('importlib.import_module') as mock_import:
            ComponentRegistrar.load_registered_components()
            mock_import.assert_called_once_with(ComponentRegistrar.REGISTERED)

    def test_load_registered_components_failure(self):
        # Test import failure
        with patch('importlib.import_module', side_effect=ImportError("Failed")):
            with self.assertRaises(ImportError):
                ComponentRegistrar.load_registered_components()

    def test_registered_components_loaded_true(self):
        # Simulate that the registered package is loaded
        sys.modules[ComponentRegistrar.REGISTERED] = MagicMock()
        self.assertTrue(ComponentRegistrar.registered_components_loaded())
        del sys.modules[ComponentRegistrar.REGISTERED]  # Clean up

    def test_registered_components_loaded_false(self):
        # Ensure the registered package is not loaded
        if ComponentRegistrar.REGISTERED in sys.modules:
            del sys.modules[ComponentRegistrar.REGISTERED]
        self.assertFalse(ComponentRegistrar.registered_components_loaded())


if __name__ == '__main__':
    unittest.main()