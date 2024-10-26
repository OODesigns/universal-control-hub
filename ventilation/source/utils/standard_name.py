import re
from utils.response import Response
from utils.status import Status
from utils.value import ValidatedValue, ValidationStrategy, StrictValidatedValue


class StandardName(ValidatedValue[str]):
    def get__strategies(self):
        return self._strategies

    def __init__(self, value):
        # Initialize the strategies for this subclass
        self._strategies = [
            StandardNameStrategy()
        ]
        super().__init__(value)


class StandardNameStrategy(ValidationStrategy):
    def validate(self, value) -> Response:
        if not re.fullmatch(r'[a-z_]+', value):
            return Response(
                status=Status.EXCEPTION,
                details="Value must contain only lowercase letters 'a-z' and underscores ('_')",
                value=None
            )
        return Response(status=Status.OK, details="Lowercase validation successful", value=value)


def sn(value: str) -> StandardName:
    return StandardName(value)

class StrictStandardName(StandardName, StrictValidatedValue[str]):
    pass

def ssn(value: str) -> StandardName:
    return StrictStandardName(value)