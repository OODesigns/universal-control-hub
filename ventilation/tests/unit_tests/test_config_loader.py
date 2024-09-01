import json
import os
import tempfile
import unittest

from config.config_loader import ConfigLoader


class TestConfigLoader(unittest.TestCase):
    def setUp(self):
        """Set up a test config loader file in a temporary directory before each test."""
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_file = os.path.join(self.test_dir.name, 'test_data.json')
        # Initialize the loader with some data
        with open(self.test_file, 'w') as f:
            json.dump({
                "name": "Alice",
                "dependencies": ["MODBUS", "AnotherDependency"],
                "single_value": "NotAnArray"
            }, f)
        self.config_loader = ConfigLoader(self.test_file)

    def tearDown(self):
        """Cleanup the temporary directory after each test."""
        self.test_dir.cleanup()

    def test_get_value(self):
        """Test that values can be retrieved correctly in read-only mode."""
        self.assertEqual(self.config_loader.get_value('name'), 'Alice')

    def test_nonexistent_key_returns_none(self):
        """Test that getting a non-existent key returns None in read-only mode."""
        self.assertIsNone(self.config_loader.get_value('nonexistent'))

    def test_get_array_returns_correct_array(self):
        """Test that get_array returns the correct array when the key exists."""
        self.assertEqual(self.config_loader.get_array('dependencies'), ["MODBUS", "AnotherDependency"])

    def test_get_array_returns_empty_list_for_nonexistent_key(self):
        """Test that get_array returns an empty list when the key does not exist."""
        self.assertEqual(self.config_loader.get_array('nonexistent'), [])

    def test_get_array_returns_empty_list_for_non_array_value(self):
        """Test that get_array returns an empty list when the key exists but is not an array."""
        self.assertEqual(self.config_loader.get_array('single_value'), [])

    def test_get_array_returns_empty_list_for_empty_array(self):
        """Test that get_array returns an empty list when the key exists but is an empty array."""
        with open(self.test_file, 'w') as f:
            json.dump({
                "empty_array": []
            }, f)
        self.config_loader = ConfigLoader(self.test_file)
        self.assertEqual(self.config_loader.get_array('empty_array'), [])


if __name__ == '__main__':
    unittest.main()
