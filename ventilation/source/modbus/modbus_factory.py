from typing import Type
from modbus.modbus import ModbusMode, ModbusInterface
from modbus.modbus_builder import ModbusBuilder
from modbus.modbus_tcp_builder import ModbusTCPBuilder
from modbus.modus_rtu_builder import ModbusRTUBuilder


class ModbusFactory:
    _registry = {}

    @classmethod
    def register_modbus(cls, mode: ModbusMode, client_class: Type[ModbusInterface]):
        """
        Registers a Modbus client class for a specific Modbus mode.

        :param mode: ModbusMode Enum (TCP or RTU)
        :param client_class: A class that implements ModbusInterface
        """
        cls._registry[mode] = client_class

    @classmethod
    def create_modbus(cls, mode: ModbusMode, builder: ModbusBuilder, **kwargs) -> ModbusInterface:
        """
        Factory method to create either a ModbusTCP or ModbusRTU instance using a ModbusBuilder.

        :param mode: ModbusMode Enum (TCP or RTU)
        :param builder: ModbusBuilder instance with common parameters
        :param kwargs: Additional parameters specific to the respective mode
        :return: An instance of ModbusInterface
        """
        client_class = cls._registry.get(mode)

        # Assert that a client_class has been registered for the given mode
        assert client_class is not None, f"No client registered for mode {mode}"

        if mode == ModbusMode.TCP:
            tcp_builder = ModbusTCPBuilder(builder, client_class=client_class)
            tcp_builder.set_ip_address(kwargs.get('ip_address'))
            tcp_builder.set_port(kwargs.get('port'))
            return tcp_builder.build()

        elif mode == ModbusMode.RTU:
            # Assuming RTUBuilder follows a similar pattern
            rtu_builder = ModbusRTUBuilder(builder, client_class=client_class)
            rtu_builder.set_baud_rate(kwargs.get('baud_rate'))
            rtu_builder.set_parity(kwargs.get('parity'))
            rtu_builder.set_stop_bits(kwargs.get('stop_bits'))
            rtu_builder.set_serial_port(kwargs.get('serial_port'))
            return rtu_builder.build()

        else:
            assert False, "Unsupported mode. Use ModbusMode.TCP or ModbusMode.RTU."
