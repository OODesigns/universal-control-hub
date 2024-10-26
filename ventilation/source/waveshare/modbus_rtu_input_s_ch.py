from modbus.modbus_values import (InputRegisterSize, HoldingRegisterSize, Timeout, Retries, ReconnectDelay, ReconnectDelayMax)
from modbus.modbus import ModbusInterface
from modbus.modus_rtu_client_builder import ModbusRTUClientBuilder
from utils.operation_response import OperationResponse
from config.config_loader import ConfigLoader

# Assuming config keys for the 8CH device
DEVICE_PORT = 'device-port'
DEVICE_BAUD_RATE = 'device-baud-rate'
DEVICE_PARITY = 'device-parity'
DEVICE_STOP_BITS = 'device-stop-bits'
DEVICE_TIMEOUT = 'device-timeout'
DEVICE_RETRIES = 'device-retries'
DEVICE_RECONNECT_DELAY = 'device-reconnect-delay'
DEVICE_RECONNECT_DELAY_MAX = 'device-reconnect-delay-max'

class ModbusRTUAnalogInput8CH:
    def __init__(self, config_loader: ConfigLoader):
        # Initialize the ModbusRTUClientBuilder with Modbus RTU specific settings
        self._modbus = (
            ModbusRTUClientBuilder()
            .set_baud_rate(config_loader.get_value(DEVICE_BAUD_RATE))  # Assumed to be part of the configuration
            .set_parity(config_loader.get_value(DEVICE_PARITY))
            .set_stop_bits(config_loader.get_value(DEVICE_STOP_BITS))
            .set_input_register_size(InputRegisterSize(8))  # 8 channels
            .set_holding_register_size(HoldingRegisterSize(8))  # Assuming 8 registers for configuration
            .set_timeout(Timeout(config_loader.get_value(DEVICE_TIMEOUT)))
            .set_retries(Retries(config_loader.get_value(DEVICE_RETRIES)))
            .set_reconnect_delay(ReconnectDelay(config_loader.get_value(DEVICE_RECONNECT_DELAY)))
            .set_reconnect_delay_max(ReconnectDelayMax(config_loader.get_value(DEVICE_RECONNECT_DELAY_MAX)))
        ).build()

    @property
    def modbus(self) -> ModbusInterface:
        return self._modbus

    async def read_input_channels(self):
        """
        Read input registers for the 8 channels. The result will be the current analog input values.
        """
        # Assuming channels 0-7 are mapped to input registers starting from address 0x0000
        # return await self.modbus.read_input_registers(0x0000, 8)  # Read 8 registers for 8 channels

    async def set_channel_mode(self, channel, mode):
        """
        Set the measurement mode for a specific channel.
        Modes can be 0-4 based on the documentation (0: 0-5V, 1: 1-5V, 2: 0-20mA, 3: 4-20mA, 4: scale code).

        if channel < 1 or channel > 8:
            raise ValueError("Channel number must be between 1 and 8")
        register_address = 0x1000 + (channel - 1)  # Each channel is mapped to 0x1000 to 0x1007
        return await self.modbus.write_holding_register(register_address, mode)
        """

    def close(self) -> OperationResponse:
        return self.modbus.disconnect()

    async def open(self) -> OperationResponse:
        return await self.modbus.connect()
