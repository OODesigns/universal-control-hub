import json
import os
import tempfile
import unittest

from config.config_factory import ConfigFactory
from config.config_loader import ConfigLoader
from config.config_store import ConfigStore


class TestConfigFactory(unittest.TestCase):
    def setUp(self):
        """Set up a temporary directory for testing the factory."""
        self.test_dir = tempfile.TemporaryDirectory()
        self.factory = ConfigFactory(self.test_dir.name)

    def tearDown(self):
        """Cleanup the temporary directory after each test."""
        self.test_dir.cleanup()

    def test_create_loader(self):
        """Test that the factory correctly creates a ConfigLoader."""
        loader = self.factory.create_loader('config.json')
        self.assertIsInstance(loader, ConfigLoader)
        expected_path = os.path.join(self.test_dir.name, 'config.json')
        self.assertEqual(loader._file_name, expected_path)

    def test_create_store(self):
        """Test that the factory correctly creates a ConfigStore."""
        store = self.factory.create_store('config.json')
        self.assertIsInstance(store, ConfigStore)
        expected_path = os.path.join(self.test_dir.name, 'config.json')
        self.assertEqual(store._file_name, expected_path)

    def test_loader_reads_existing_config(self):
        """Test that a ConfigLoader can read an existing config file."""
        config_file = os.path.join(self.test_dir.name, 'config.json')
        with open(config_file, 'w') as f:
            json.dump({"name": "Alice"}, f)

        loader = self.factory.create_loader('config.json')
        self.assertEqual(loader.get_value('name'), 'Alice')

    def test_store_can_write_and_read(self):
        """Test that a ConfigStore can write and then read back data."""
        store = self.factory.create_store('config.json')
        store.set_value('name', 'Bob')

        loader = self.factory.create_loader('config.json')
        self.assertEqual(loader.get_value('name'), 'Bob')

if __name__ == '__main__':
    unittest.main()