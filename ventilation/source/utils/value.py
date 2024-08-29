from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any

class Value:
    """
    A base class to represent a generic value. Provides comparison methods for equality, less than,
    and less than or equal to comparisons between instances of derived classes.
    """
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        """Returns the stored value."""
        return self._value

    def __eq__(self, other):
        """Checks equality between two Value instances."""
        if type(self) is type(other):
            return self.value == other.value
        return False

    def __lt__(self, other):
        """Checks if this value is less than another."""
        if type(self) is type(other):
            return self.value < other.value
        return False

    def __le__(self, other):
        """Checks if this value is less than or equal to another."""
        if type(self) is type(other):
            return self.value <= other.value
        return False

class ValueStatus(Enum):
    """
    Enum to represent the status of a validation process.
    """
    OK = 0
    EXCEPTION = 1

@dataclass
class ValidatedResponse:
    """
    Data class to encapsulate the result of a validation process.

    Attributes:
        status: The status of the validation (OK or EXCEPTION).
        details: A message detailing the result of the validation.
        value: The value being validated.
    """
    status: ValueStatus
    details: str
    value: Any

class ValidatedValue(Value, ABC):
    """
    A base class that represents a value which must be validated. Subclasses are required to implement
    the validate method to perform validation and return a ValidatedResult.

    Attributes:
        _status: The status of the validation.
        _details: Additional details regarding the validation status.
    """
    def __init__(self, validated_value=None):
        result = self.__class__.validate(validated_value)
        super().__init__(value=result.value)
        self._status = result.status
        self._details = result.details

    @classmethod
    @abstractmethod
    def validate(cls, validated_value) -> ValidatedResponse:
        """
        Abstract method to validate the value. Subclasses must implement this to return a ValidatedResult.

        Args:
            validated_value: The value to be validated.

        Returns:
            A ValidatedResult object containing the status, details, and the validated value.
        """
        pass

    @property
    def status(self) -> ValueStatus:
        """Returns the status of the validation."""
        return self._status

    @property
    def details(self) -> str:
        """Returns the details of the validation status."""
        return self._details

    @property
    def value(self):
        """Returns the value if validation was successful, otherwise raises a ValueError."""
        if self._status == ValueStatus.EXCEPTION:
            raise ValueError(f"Cannot access value: {self.details}")
        return self._value

    def _same_status(self, other):
        """Checks if another ValidatedValue instance has the same validation status."""
        return self.status == other.status

    def __eq__(self, other):
        """Checks equality considering both validation status and value."""
        return self._same_status(other) and super().__eq__(other)

    def __lt__(self, other):
        """Checks if this value is less than another, considering validation status."""
        return self._same_status(other) and super().__lt__(other)

    def __le__(self, other):
        """Checks if this value is less than or equal to another, considering validation status."""
        return self._same_status(other) and super().__le__(other)

class StrictValidatedValue(ValidatedValue, ABC):
    """
    A stricter version of ValidatedValue that raises an exception immediately if the validation fails.
    """
    def __init__(self, validated_value=None):
        super().__init__(validated_value)
        if self.status == ValueStatus.EXCEPTION:
            raise ValueError(f"Validation failed for value '{validated_value}': {self.details}")

class RangeValidatedValue(ValidatedValue):
    """
    A base class that provides range validation for numeric values.
    Subclasses should define `valid_types`, `low_value`, and `high_value`.

    """
    high_value = None
    low_value = None
    valid_types = None

    @classmethod
    def validate(cls, value) -> ValidatedResponse:
        if not (type(value) in cls.valid_types) or not (cls.low_value <= value <= cls.high_value):
            return ValidatedResponse(
                status=ValueStatus.EXCEPTION,
                details=f"{cls.__name__} must be a {cls.valid_types} between {cls.low_value} and {cls.high_value}, got {value}",
                value=None
            )
        return ValidatedResponse(
            status=ValueStatus.OK,
            details="",
            value=value
        )