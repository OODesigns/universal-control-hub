from pymodbus.client import AsyncModbusTcpClient, ModbusBaseClient
from utils.value import ValidatedResponse, ValueStatus

class ModbusClientManager:
    def __init__(self, client: ModbusBaseClient):
        """
        Initialize the ModbusClientManager with a Modbus client.

        :param client: An instance of a ModbusBaseClient.
        """
        self.client = client

    async def connect(self) -> ValidatedResponse:
        """
        Connect to the Modbus server.

        :return: A ValidatedResponse indicating the status of the connection.
        """
        try:
            await self.client.connect()
            if self.client.connected:
                return ValidatedResponse(
                    status=ValueStatus.OK,
                    details="Connected successfully.",
                    value=None
                )
            else:
                return ValidatedResponse(
                    status=ValueStatus.EXCEPTION,
                    details="Failed to connect to the server.",
                    value=None
                )
        except Exception as e:
            return ValidatedResponse(
                status=ValueStatus.EXCEPTION,
                details=f"Error occurred during connection: {str(e)}",
                value=None
            )

    def disconnect(self) -> ValidatedResponse:
        """
        Disconnect from the Modbus server.

        :return: A ValidatedResponse indicating the status of the disconnection.
        """
        try:
            if self.client is not None and self.client.connected:
                self.client.close()  # No await since close is not async
                return ValidatedResponse(
                    status=ValueStatus.OK,
                    details="Disconnected successfully.",
                    value=None
                )
            else:
                return ValidatedResponse(
                    status=ValueStatus.EXCEPTION,
                    details="Client was not connected or was already closed.",
                    value=None
                )
        except Exception as e:
            return ValidatedResponse(
                status=ValueStatus.EXCEPTION,
                details=f"Error occurred during disconnect: {str(e)}",
                value=None
            )

    async def reconnect(self) -> ValidatedResponse:
        """
        Reconnect to the Modbus server by first disconnecting and then connecting again.

        :return: A ValidatedResponse indicating the status of the reconnection.
        """
        disconnect_result = self.disconnect()
        if disconnect_result.status == ValueStatus.OK:
            return await self.connect()
        else:
            return ValidatedResponse(
                status=ValueStatus.EXCEPTION,
                details=f"Reconnection failed: {disconnect_result.details}",
                value=None
            )
