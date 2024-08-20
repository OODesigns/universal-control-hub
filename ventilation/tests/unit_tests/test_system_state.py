import unittest
import time
from types import MappingProxyType

from state.system_state import SystemState


class TestSystemState(unittest.TestCase):

    def setUp(self):
        # Sample data for testing
        self.sensor_data = {'temp1': 25.0, 'humidity1': 60}
        self.triggered_rules = {'rule1': 'Temperature out of range'}
        self.operational_states = {
            'mvhr_powered_on': True,
            'relay_purging_enabled': False,
            'motor_speed': 1500,
            'rh_trigger_value': 60,
            'pm25_trigger_value': 35,
            'voc_trigger_value': 200
        }

    def test_auto_set_timestamp(self):
        """Test that the timestamp is automatically set to the current time if not provided."""
        state = SystemState(
            sensor_data=self.sensor_data,
            triggered_rules=self.triggered_rules,
            operational_states=self.operational_states
        )
        now = time.time()
        self.assertTrue(now - state.timestamp < 1, "Timestamp should be close to the current time")

    def test_set_timestamp_from_external_source(self):
        """Test that the timestamp can be set from an external source."""
        external_timestamp = 1656349263.0  # Example timestamp from a file
        state = SystemState(
            sensor_data=self.sensor_data,
            triggered_rules=self.triggered_rules,
            operational_states=self.operational_states,
            timestamp=external_timestamp
        )
        self.assertEqual(state.timestamp, external_timestamp, "Timestamp should match the provided external value")

    def test_get_sensor_value(self):
        """Test retrieval of sensor data."""
        state = SystemState(
            sensor_data=self.sensor_data,
            triggered_rules=self.triggered_rules,
            operational_states=self.operational_states
        )
        self.assertEqual(state.get_sensor_value('temp1'), 25.0)
        self.assertEqual(state.get_sensor_value('humidity1'), 60)
        self.assertIsNone(state.get_sensor_value('nonexistent_sensor'))

    def test_get_triggered_rule(self):
        """Test retrieval of triggered rules."""
        state = SystemState(
            sensor_data=self.sensor_data,
            triggered_rules=self.triggered_rules,
            operational_states=self.operational_states
        )
        self.assertEqual(state.get_triggered_rule('rule1'), 'Temperature out of range')
        self.assertIsNone(state.get_triggered_rule('nonexistent_rule'))

    def test_get_operational_state(self):
        """Test retrieval of operational states."""
        state = SystemState(
            sensor_data=self.sensor_data,
            triggered_rules=self.triggered_rules,
            operational_states=self.operational_states
        )
        self.assertTrue(state.get_operational_state('mvhr_powered_on'))
        self.assertFalse(state.get_operational_state('relay_purging_enabled'))
        self.assertEqual(state.get_operational_state('motor_speed'), 1500)
        self.assertIsNone(state.get_operational_state('nonexistent_state'))

    def test_immutability(self):
        """Test that the SystemState is immutable."""
        state = SystemState(
            sensor_data=self.sensor_data,
            triggered_rules=self.triggered_rules,
            operational_states=self.operational_states
        )
        with self.assertRaises(TypeError):
            state.sensor_data['temp1'] = 30.0

        with self.assertRaises(TypeError):
            state.operational_states['mvhr_powered_on'] = False

        with self.assertRaises(TypeError):
            state.triggered_rules['rule1'] = 'Another rule'

    def test_empty_initialization(self):
        """Test that SystemState can be initialized with empty data."""
        state = SystemState()
        self.assertEqual(state.sensor_data, MappingProxyType({}))
        self.assertEqual(state.triggered_rules, MappingProxyType({}))
        self.assertEqual(state.operational_states, MappingProxyType({}))

    def test_serialization(self):
        """Test serialization to and from JSON."""
        state = SystemState(
            sensor_data=self.sensor_data,
            triggered_rules=self.triggered_rules,
            operational_states=self.operational_states
        )
        json_str = state.to_json()
        loaded_state = SystemState.from_json(json_str)
        self.assertEqual(loaded_state.sensor_data, state.sensor_data)
        self.assertEqual(loaded_state.triggered_rules, state.triggered_rules)
        self.assertEqual(loaded_state.operational_states, state.operational_states)
        self.assertEqual(loaded_state.timestamp, state.timestamp)

if __name__ == '__main__':
    unittest.main()
