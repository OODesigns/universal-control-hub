from devices.device_factory import DeviceFactory
from modbus.modbus import ModbusMode
from modbus.modbus_builder import ModbusBuilder
from modbus.modbus_tcp_builder import ModbusTCPBuilder
from modbus.modus_rtu_builder import ModbusRTUBuilder
from modbus.pymodbus.modus_client import ModbusClient


@DeviceFactory.register_dependency('modbus')
class ModbusFactory:
    @classmethod
    def create_modbus(cls, mode: ModbusMode, builder: ModbusBuilder, **kwargs) -> ModbusClient:
        """
        Factory method to create either a ModbusTCP or ModbusRTU instance using a ModbusBuilder.

        :param mode: ModbusMode Enum (TCP or RTU)
        :param builder: ModbusBuilder instance with common parameters
        :param kwargs: Additional parameters specific to the respective mode
        :return: ModbusTCP or ModbusRTU instance
        """
        if mode == ModbusMode.TCP:
            tcp_builder = ModbusTCPBuilder(builder)
            tcp_builder.set_ip_address(kwargs.get('ip_address'))
            tcp_builder.set_port(kwargs.get('port'))
            return tcp_builder.build()

        elif mode == ModbusMode.RTU:
            rtu_builder = ModbusRTUBuilder(builder)
            rtu_builder.set_baud_rate(kwargs.get('baud_rate'))
            rtu_builder.set_parity(kwargs.get('parity'))
            rtu_builder.set_stop_bits(kwargs.get('stop_bits'))
            rtu_builder.set_serial_port(kwargs.get('serial_port'))
            return rtu_builder.build()

        else:
            raise ValueError("Unsupported mode. Use ModbusMode.TCP or ModbusMode.RTU.")