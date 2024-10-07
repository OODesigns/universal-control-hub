import json
from typing import Optional, List, Dict, Any

from state.system_state import SystemState


class StateManager:
    def __init__(self, file_path: str):
        self._current_state: Optional[SystemState] = None  # Allow None initially
        self._state_history: List[SystemState] = []
        self.file_path = file_path

        # Load existing states from the file if they exist
        self._load_state_history()

    def update_state(self, sensor_data: Dict[str, Any] = None,
                     triggered_rules: Dict[str, str] = None,
                     operational_states: Dict[str, Any] = None,
                     timestamp: float = None):
        """
        Update the system state by appending changes to the last known state.
        Only the changes provided will be updated; the rest of the state will remain as it was.

        Args:
            sensor_data (Dict[str, Any], optional): New sensor data to update.
            triggered_rules (Dict[str, str], optional): New triggered rules to update.
            operational_states (Dict[str, Any], optional): New operational states to update.
            timestamp (float, optional): The timestamp for the new state. If not provided,
                                         it will be set to the current time.
        """
        if self._current_state is None:
            self._initialize_new_state(sensor_data, triggered_rules, operational_states, timestamp)
        else:
            self._update_existing_state(sensor_data, triggered_rules, operational_states, timestamp)

    def _initialize_new_state(self, sensor_data, triggered_rules, operational_states, timestamp):
        """Initialize the system state when there's no current state."""
        self._current_state = SystemState(
            sensor_data=sensor_data or {},
            triggered_rules=triggered_rules or {},
            operational_states=operational_states or {},
            timestamp=timestamp
        )
        # Add the initial state to the history
        self._save_current_state_to_history()

    def _update_existing_state(self, sensor_data, triggered_rules, operational_states, timestamp):
        """Update the existing state with new data."""
        new_sensor_data = self._merge_data(self._current_state.sensor_data, sensor_data)
        new_triggered_rules = self._merge_data(self._current_state.triggered_rules, triggered_rules)
        new_operational_states = self._merge_data(self._current_state.operational_states, operational_states)

        new_state = SystemState(
            sensor_data=new_sensor_data,
            triggered_rules=new_triggered_rules,
            operational_states=new_operational_states,
            timestamp=timestamp  # Use provided timestamp or default to current time
        )

        # Update to the new state Save the current state to the history
        self._current_state = new_state
        self._save_current_state_to_history()

    @classmethod
    def _merge_data(cls, current_data: Dict[str, Any], new_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Merge the current state data with the new data.
        If the same key exists in both, the value from the new data will override the old value.
        """
        return {**current_data, **(new_data or {})}

    def _save_current_state_to_history(self):
        """Append the current state to the state history and save it to the file."""
        self._state_history.append(self._current_state)
        self._write_state_to_file(self._current_state)

    @property
    def current_state(self) -> Optional[SystemState]:
        return self._current_state

    def get_state_history(self) -> List[SystemState]:
        return self._state_history

    def clear_state_history(self):
        self._state_history = []
        with open(self.file_path, 'w') as f:
            f.write("")

    def _write_state_to_file(self, state: SystemState):
        """Serialize the state to JSON and append it to the file."""
        with open(self.file_path, 'a') as f:
            f.write(json.dumps(state.to_dict()) + "\n")

    def _load_state_history(self):
        """Load state history from a file, if the file exists."""
        try:
            with open(self.file_path, 'r') as f:
                for line in f:
                    self._load_state_from_line(line)
        except FileNotFoundError:
            # If the file does not exist, start with an empty history
            pass

    def _load_state_from_line(self, line: str):
        """Load a single state from a line of JSON and append it to the state history."""
        self._state_history.append(SystemState.from_dict(json.loads(line)))
