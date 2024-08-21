import unittest

from devices.modbus import ModbusTCP, ModbusRTU, ParityType, ModbusFactory, ModbusMode
from utils.tcp_values import IPAddress, Port, Timeout
from utils.rtu_values import BaudRate, StopBits

class TestModbusClasses(unittest.TestCase):

    # Test for ModbusTCP class
    def test_modbus_tcp_valid(self):
        ip_address = IPAddress('192.168.1.1')
        port = Port(502)
        timeout = Timeout(1)

        modbus_tcp = ModbusTCP(
            ip_address=ip_address,
            port=port,
            timeout=timeout,
            coil_size=25,
            discrete_input_size=72,
            input_register_size=51,
            holding_register_size=182
        )
        self.assertEqual(modbus_tcp._ip_address.value, '192.168.1.1')
        self.assertEqual(modbus_tcp._port.value, 502)
        self.assertEqual(modbus_tcp._timeout.value, 1)
        self.assertEqual(modbus_tcp._coil_size, 25)
        self.assertEqual(modbus_tcp._discrete_input_size, 72)
        self.assertEqual(modbus_tcp._input_register_size, 51)
        self.assertEqual(modbus_tcp._holding_register_size, 182)

    def test_modbus_tcp_invalid_sizes(self):
        ip_address = IPAddress('192.168.1.1')
        port = Port(502)
        timeout = Timeout(1)

        with self.assertRaises(ValueError):
            ModbusTCP(
                ip_address=ip_address,
                port=port,
                timeout=timeout,
                coil_size=-1,  # Invalid negative size
                discrete_input_size=72,
                input_register_size=51,
                holding_register_size=182
            )

        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            ModbusTCP(
                ip_address=ip_address,
                port=port,
                timeout=timeout,
                coil_size=25,
                discrete_input_size='72',  # Invalid type (string instead of int)
                input_register_size=51,
                holding_register_size=182
            )

    # Test for ModbusRTU class
    def test_modbus_rtu_valid(self):
        baud_rate = BaudRate(9600)
        stop_bits = StopBits(1)

        modbus_rtu = ModbusRTU(
            baud_rate=baud_rate,
            parity=ParityType.NONE,
            stop_bits=stop_bits,
            coil_size=25,
            discrete_input_size=72,
            input_register_size=51,
            holding_register_size=182
        )
        self.assertEqual(modbus_rtu._baud_rate.value, 9600)
        self.assertEqual(modbus_rtu._parity, ParityType.NONE)
        self.assertEqual(modbus_rtu._stop_bits.value, 1)
        self.assertEqual(modbus_rtu._coil_size, 25)
        self.assertEqual(modbus_rtu._discrete_input_size, 72)
        self.assertEqual(modbus_rtu._input_register_size, 51)
        self.assertEqual(modbus_rtu._holding_register_size, 182)

    def test_modbus_rtu_invalid_sizes(self):
        baud_rate = BaudRate(9600)
        stop_bits = StopBits(1)
        timeout = Timeout(1)

        with self.assertRaises(ValueError):
            ModbusRTU(
                baud_rate=baud_rate,
                parity=ParityType.NONE,
                stop_bits=stop_bits,
                coil_size=-10,  # Invalid negative size
                discrete_input_size=72,
                input_register_size=51,
                holding_register_size=182
            )

        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            ModbusRTU(
                baud_rate=baud_rate,
                parity=ParityType.NONE,
                stop_bits=stop_bits,
                coil_size=25,
                discrete_input_size=72,
                input_register_size='51',  # Invalid type (string instead of int)
                holding_register_size=182
            )

    # Test for ModbusFactory
    def test_modbus_factory_tcp(self):
        ip_address = IPAddress('192.168.1.1')
        port = Port(502)
        timeout = Timeout(1)

        modbus = ModbusFactory.create_modbus(
            mode=ModbusMode.TCP,
            coil_size=25,
            discrete_input_size=72,
            input_register_size=51,
            holding_register_size=182,
            ip_address=ip_address,
            port=port,
            timeout=timeout
        )
        self.assertIsInstance(modbus, ModbusTCP)
        self.assertEqual(modbus._coil_size, 25)
        self.assertEqual(modbus._ip_address.value, '192.168.1.1')

    def test_modbus_factory_rtu(self):
        baud_rate = BaudRate(9600)
        stop_bits = StopBits(1)

        modbus = ModbusFactory.create_modbus(
            mode=ModbusMode.RTU,
            baud_rate=baud_rate,
            parity=ParityType.NONE,
            stop_bits=stop_bits,
            coil_size=25,
            discrete_input_size=72,
            input_register_size=51,
            holding_register_size=182
        )
        self.assertIsInstance(modbus, ModbusRTU)
        self.assertEqual(modbus._coil_size, 25)
        self.assertEqual(modbus._baud_rate.value, 9600)

    def test_modbus_factory_invalid_mode(self):
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            ModbusFactory.create_modbus(
                mode="InvalidMode",  # Invalid mode
                coil_size=25,
                discrete_input_size=72,
                input_register_size=51,
                holding_register_size=182
            )

if __name__ == '__main__':
    unittest.main()
