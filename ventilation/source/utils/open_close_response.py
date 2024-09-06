from utils.operation_response import OperationResponse


class OpenResponse(OperationResponse):
    """
    A response for handling the result of opening a connection or SPI interface.
    Inherits from OperationResponse for general status handling.
    """
    pass  # You can extend this if more details are needed for open.


class CloseResponse(OperationResponse):
    """
    A response for handling the result of closing a connection or SPI interface.
    Inherits from OperationResponse for general status handling.
    """
    pass  # You can extend this if more details are needed for close.
