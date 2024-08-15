import json
import os
import tempfile
import unittest
from unittest.mock import patch

from config.config_store import ConfigStore


class TestConfigStore(unittest.TestCase):
    def setUp(self):
        """Set up a test store file in a temporary directory before each test."""
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_file = os.path.join(self.test_dir.name, 'test_data.json')
        self.store = ConfigStore(self.test_file)

    def tearDown(self):
        """Cleanup the temporary directory after each test."""
        self.test_dir.cleanup()

    def test_set_and_get(self):
        """Test that values can be set and retrieved correctly."""
        self.store.set_value('name', 'Alice')
        self.assertEqual(self.store.get_value('name'), 'Alice')

    def test_overwrite_existing_key(self):
        """Test that setting a value for an existing key overwrites it."""
        self.store.set_value('name', 'Alice')
        self.store.set_value('name', 'Bob')
        self.assertEqual(self.store.get_value('name'), 'Bob')

    def test_nonexistent_key_returns_none(self):
        """Test that getting a non-existent key returns None."""
        self.assertIsNone(self.store.get_value('nonexistent'))

    def test_data_integrity_after_save(self):
        """Test that the data is correctly saved and reloaded."""
        # Set a key-value pair
        self.store.set_value('key1', 'value1')

        # Load the data directly from the JSON file
        with open(self.test_file, 'r') as f:
            saved_data = json.load(f)

        # Check that the saved data matches the in-memory data
        self.assertEqual(self.store._data, saved_data)

    @patch("json.load")
    def test_data_mismatch_raises_error(self, mock_json_load):
        """Test that a data mismatch raises an IOError."""
        mock_json_load.side_effect = lambda x:{"key1": "corrupted_data"}

        # Check if IOError is raised due to data mismatch
        with self.assertRaises(IOError):
            self.store.set_value('key1', 'value1')
