from dataclasses import dataclass

from pymodbus.client import ModbusBaseClient
from utils.operation_response import OperationStatus, OperationResponse


@dataclass(frozen=True)
class ModbusConnectionManager:
    client: ModbusBaseClient

    async def connect(self) -> OperationResponse:
        try:
            await self.client.connect()
            if self.client.connected:
                return OperationResponse(
                    status=OperationStatus.OK,
                    details="Connected successfully."
                )
            else:
                return OperationResponse(
                    status=OperationStatus.FAILED,
                    details="Failed to connect to the server."
                )
        except Exception as e:
            return OperationResponse(
                status=OperationStatus.EXCEPTION,
                details=f"Error occurred during connection: {str(e)}"
            )

    def disconnect(self) -> OperationResponse:
        try:
            if self.client is not None and self.client.connected:
                self.client.close()  # No await since close is not async
                return OperationResponse(
                    status=OperationStatus.OK,
                    details="Disconnected successfully."
                )
            else:
                return OperationResponse(
                    status=OperationStatus.EXCEPTION,
                    details="Client was not connected or was already closed."
                )
        except Exception as e:
            return OperationResponse(
                status=OperationStatus.EXCEPTION,
                details=f"Error occurred during disconnect: {str(e)}"
            )