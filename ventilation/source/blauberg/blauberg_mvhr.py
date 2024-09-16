from blauberg.blauberg_mvhr_state import BlaubergMVHRState
from blauberg.blauberg_registers import (CoilRegister, DiscreteInputs,
                                         InputRegisters, HoldingRegister)
from config.config_loader import ConfigLoader
from devices.mvhr import MVHR
from modbus.modbus import ModbusInterface
from modbus.modbus_tcp_builder import ModbusTCPBuilder
from mvhr_state import MVHRStateInterface
from modbus.tcp_values import IPAddress, Port
from utils.operation_response import OperationResponse
from modbus.modbus_values import (DiscreteInputSize, ReconnectDelay,
                                  HoldingRegisterSize, Timeout, Retries,
                                  InputRegisterSize, ReconnectDelayMax, CoilSize)

MVHR_PORT = 'mvhr-port'
MVHR_IP_ADDRESS = 'mvhr-ip-address'
MVHR_TIMEOUT = 'mvhr-timeout'
MVHR_RETRIES = 'mvhr-retries'
MVHR_RECONNECT_DELAY = 'mvhr-reconnect-delay'
MVHR_RECONNECT_DELAY_MAX = 'mvhr-reconnect-delay-max'

class BlaubergMVHR(MVHR):
    def __init__(self, config_loader: ConfigLoader):
        super().__init__(config_loader)

       # Use the factory to create the Modbus interface
        self._modbus =(
            ModbusTCPBuilder()
            .set_coil_size(CoilSize(CoilRegister.CL_SIZE.value))
            .set_discrete_input_size(DiscreteInputSize(DiscreteInputs.DI_SIZE.value))
            .set_input_register_size(InputRegisterSize(InputRegisters.IR_SIZE.value))
            .set_holding_register_size(HoldingRegisterSize(HoldingRegister.HR_SIZE.value))
            # Set modbus settings from the configuration loader
            .set_timeout(Timeout(config_loader.get_value(MVHR_TIMEOUT)))
            .set_retries(Retries(config_loader.get_value(MVHR_RETRIES)))
            .set_reconnect_delay(ReconnectDelay(config_loader.get_value(MVHR_RECONNECT_DELAY)))
            .set_reconnect_delay_max(ReconnectDelayMax(config_loader.get_value(MVHR_RECONNECT_DELAY_MAX)))
            # Set TPC Part
            .set_ip_address(IPAddress(config_loader.get_value(MVHR_IP_ADDRESS)))
            .set_port(Port(config_loader.get_value(MVHR_PORT)))
        ).build()


    @property
    def modbus(self) -> ModbusInterface:
        return self._modbus

    async def read(self) -> MVHRStateInterface:
        return BlaubergMVHRState(await self.modbus.read())

    def stop(self) -> OperationResponse:
        return self.modbus.disconnect()

    async def start(self) -> OperationResponse:
        return await self.modbus.connect()
