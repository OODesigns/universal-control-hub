from dataclasses import dataclass

from pymodbus.client import ModbusBaseClient
from utils.connection_reponse import ConnectionResponse
from utils.operation_response import OperationStatus


@dataclass(frozen=True)
class ModbusConnectionManager:
    client: ModbusBaseClient

    async def connect(self) -> ConnectionResponse:
        try:
            await self.client.connect()
            if self.client.connected:
                return ConnectionResponse(
                    status=OperationStatus.OK,
                    details="Connected successfully."
                )
            else:
                return ConnectionResponse(
                    status=OperationStatus.FAILED,
                    details="Failed to connect to the server."
                )
        except Exception as e:
            return ConnectionResponse(
                status=OperationStatus.EXCEPTION,
                details=f"Error occurred during connection: {str(e)}"
            )

    def disconnect(self) -> ConnectionResponse:
        try:
            if self.client is not None and self.client.connected:
                self.client.close()  # No await since close is not async
                return ConnectionResponse(
                    status=OperationStatus.OK,
                    details="Disconnected successfully."
                )
            else:
                return ConnectionResponse(
                    status=OperationStatus.EXCEPTION,
                    details="Client was not connected or was already closed."
                )
        except Exception as e:
            return ConnectionResponse(
                status=OperationStatus.EXCEPTION,
                details=f"Error occurred during disconnect: {str(e)}"
            )