from dataclasses import dataclass

from utils.response import Response
from utils.status import Status
from utils.value import ValidationStrategy


@dataclass(frozen=True)
class ExceptionCascade(ValidationStrategy):
    response: Response
    """
    A strategy that checks if a Response object contains an error and cascades it.
    If the status is OK, it lets other strategies run.
    """
    def validate(self, value) -> Response:
        if self.response.status == Status.OK:
            # If all OK, update the passed value and return it
            return Response(
                status=self.response.status,
                details=self.response.details,
                value=value
            )
        return self.response  # If there is an error, cascade the error response back immediately

