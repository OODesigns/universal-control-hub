import json
import unittest
import os

from state.state_manager import StateManager
from state.system_state import SystemState


class TestStateManager(unittest.TestCase):

    def setUp(self):
        # A temporary file path for testing
        self.file_path = 'test_state_history.json'
        self.state_manager = StateManager(file_path=self.file_path)

    def tearDown(self):
        # Clean up the test file after each test
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_initial_state_is_saved_to_history(self):
        """Test that the initial state is saved to the history."""
        self.state_manager.update_state(sensor_data={'temp1': 25.0}, operational_states={'mvhr_powered_on': True})

        # The history should have 1 entry after the first update
        history = self.state_manager.get_state_history()
        self.assertEqual(len(history), 1)

        # Verify the content of the initial state in history
        initial_state = history[0]
        self.assertEqual(initial_state.get_sensor_value('temp1'), 25.0)
        self.assertTrue(initial_state.get_operational_state('mvhr_powered_on'))

    def test_update_and_save_state_to_history(self):
        """Test that each update is saved to the history."""
        # Initial update
        self.state_manager.update_state(sensor_data={'temp1': 25.0})
        # Second update
        self.state_manager.update_state(sensor_data={'temp2': 27.0})

        # The history should have 2 entries after two updates
        history = self.state_manager.get_state_history()
        self.assertEqual(len(history), 2)

        # Verify the content of the first state in history
        first_state = history[0]
        self.assertEqual(first_state.get_sensor_value('temp1'), 25.0)
        self.assertIsNone(first_state.get_sensor_value('temp2'))

        # Verify the content of the second state in history
        second_state = history[1]
        self.assertEqual(second_state.get_sensor_value('temp1'), 25.0)
        self.assertEqual(second_state.get_sensor_value('temp2'), 27.0)

    def test_clear_state_history(self):
        """Test clearing the state history."""
        self.state_manager.update_state(sensor_data={'temp1': 25.0})
        self.state_manager.update_state(sensor_data={'temp2': 27.0})

        # Clear history
        self.state_manager.clear_state_history()
        history = self.state_manager.get_state_history()

        self.assertEqual(len(history), 0)
        self.assertIsNotNone(self.state_manager.current_state)  # Current state should remain

    def test_save_and_load_state(self):
        """Test saving the current state to a file and loading it back."""
        self.state_manager.update_state(sensor_data={'temp1': 25.0})
        self.state_manager.update_state(sensor_data={'temp2': 27.0})

        # Reinitialize state manager to load from file
        new_state_manager = StateManager(file_path=self.file_path)
        history = new_state_manager.get_state_history()

        self.assertEqual(len(history), 2)
        self.assertEqual(history[0].get_sensor_value('temp1'), 25.0)
        self.assertIsNone(history[0].get_sensor_value('temp2'))
        self.assertEqual(history[1].get_sensor_value('temp1'), 25.0)
        self.assertEqual(history[1].get_sensor_value('temp2'), 27.0)

    def test_serialization_of_current_state(self):
        """Test that the current state can be correctly serialized and deserialized."""
        self.state_manager.update_state(sensor_data={'temp1': 25.0}, triggered_rules={'rule1': 'Overheat'})
        current_state = self.state_manager.current_state
        serialized_state = current_state.to_json()

        deserialized_state = SystemState.from_json(serialized_state)
        self.assertEqual(deserialized_state.get_sensor_value('temp1'), 25.0)
        self.assertEqual(deserialized_state.get_triggered_rule('rule1'), 'Overheat')

    def test_loading_state_from_file(self):
        """Test that state history is correctly loaded from a file."""
        # Prepare some state data and write it to the file manually
        state_data = {
            'sensor_data': {'temp1': 25.0},
            'triggered_rules': {'rule1': 'Overheat'},
            'operational_states': {'mvhr_powered_on': True},
            'timestamp': 1656349263.0
        }
        with open(self.file_path, 'w') as f:
            f.write(json.dumps(state_data) + "\n")

        # Reinitialize state manager to load from the file
        new_state_manager = StateManager(file_path=self.file_path)
        history = new_state_manager.get_state_history()

        self.assertEqual(len(history), 1)
        self.assertEqual(history[0].get_sensor_value('temp1'), 25.0)
        self.assertEqual(history[0].get_triggered_rule('rule1'), 'Overheat')
        self.assertTrue(history[0].get_operational_state('mvhr_powered_on'))
        self.assertEqual(history[0].timestamp, 1656349263.0)

if __name__ == '__main__':
    unittest.main()
