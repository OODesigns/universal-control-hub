import json
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Dict, Any, Optional
import time


@dataclass(frozen=True)
class SystemState:
    """
       Represents the state of the system at a specific point in time, capturing sensor data,
       operational states, and any triggered rules.

       Fields:
           - sensor_data (Dict[str, Any]):
               A dictionary holding the sensor readings where the key is the sensor name (e.g., "temp1",
               "humidity1") and the value is the corresponding reading (e.g., 25.0 for temperature, 60 for humidity).

           - triggered_rules (Dict[str, str]):
               A dictionary storing information about rules that were triggered. The key is the name
               of the rule, and the value is a description or action taken because of that rule being triggered.

           - operational_states (Dict[str, Any]):
               A dictionary storing various operational states of the system, such as whether the MVHR
               is powered on, relay states, motor speeds, and trigger values for sensors like RH (Relative Humidity),
               PM2.5, VOC, etc.

           - timestamp (float):
               A floating-point number representing the time (in seconds since the epoch) when the
               SystemState instance was created. This can be set from an external source (e.g., a file)
               or defaults to the current time.

       Notes:
           - `field(default_factory=dict)` is used for `triggered_rules` and `operational_states` to
             ensure that these fields are always initialized as dictionaries, even if the user does not
             provide any values. This prevents potential issues with mutable default arguments and ensures
             that each instance of `SystemState` has its own independent dictionary for these fields.

           - The `timestamp` field is excluded from the `__init__` method by using `init=False`. This is
             necessary because we want to automatically set the `timestamp` to the current time when an instance
             of SystemState is created, rather than requiring the user to pass it in. The `__post_init__` method
             is then used to set the `timestamp` after the object is instantiated.
       """

    sensor_data: Dict[str, Any] = field(default_factory=dict)  # Initially passed as a regular dict
    triggered_rules: Dict[str, str] = field(default_factory=dict)  # Keep track of rules that were triggered
    operational_states: Dict[str, Any] = field(default_factory=dict)  # Store operational system states
    timestamp: Optional[float] = None

    def __post_init__(self):
        # Set the timestamp to current time if not provided
        if self.timestamp is None:
            object.__setattr__(self, 'timestamp', time.time())

        # Convert mutable dictionaries to immutable MappingProxyType
        object.__setattr__(self, 'sensor_data', MappingProxyType(self.sensor_data))
        object.__setattr__(self, 'triggered_rules', MappingProxyType(self.triggered_rules))
        object.__setattr__(self, 'operational_states', MappingProxyType(self.operational_states))

    def get_sensor_value(self, sensor_name: str) -> Any:
        return self.sensor_data.get(sensor_name)

    def get_triggered_rule(self, rule_name: str) -> str:
        return self.triggered_rules.get(rule_name)

    def get_operational_state(self, state_name: str) -> Any:
        return self.operational_states.get(state_name)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the SystemState to a dictionary for easy JSON serialization."""
        return {
            'sensor_data': dict(self.sensor_data),  # Convert MappingProxyType to dict
            'triggered_rules': dict(self.triggered_rules),  # Convert MappingProxyType to dict
            'operational_states': dict(self.operational_states),  # Convert MappingProxyType to dict
            'timestamp': self.timestamp
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SystemState':
        """Create a SystemState object from a dictionary."""
        return cls(
            sensor_data=data.get('sensor_data', {}),
            triggered_rules=data.get('triggered_rules', {}),
            operational_states=data.get('operational_states', {}),
            timestamp=data.get('timestamp')
        )

    def to_json(self) -> str:
        """Serialize the SystemState to a JSON string."""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> 'SystemState':
        """Deserialize a SystemState object from a JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)
