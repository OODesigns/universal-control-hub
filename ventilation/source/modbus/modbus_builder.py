from modbus.modbus_values import CoilSize, DiscreteInputSize, InputRegisterSize, HoldingRegisterSize, Retries, ReconnectDelay, ReconnectDelayMax, Timeout

class ModbusBuilder:
    def __init__(self, builder=None):
        if builder:
            assert isinstance(builder, ModbusBuilder), "Expected builder to be an instance of ModbusBuilder"
            # Use setter methods to copy values from the provided builder
            self.set_coil_size(builder.coil_size)
            self.set_discrete_input_size(builder.discrete_input_size)
            self.set_input_register_size(builder.input_register_size)
            self.set_holding_register_size(builder.holding_register_size)
            self.set_timeout(builder.timeout)
            self.set_retries(builder.retries)
            self.set_reconnect_delay(builder.reconnect_delay)
            self.set_reconnect_delay_max(builder.reconnect_delay_max)
        else:
            # Initialize attributes to None or appropriate defaults
            self._coil_size = None
            self._discrete_input_size = None
            self._input_register_size = None
            self._holding_register_size = None
            self._timeout = None
            self._retries = None
            self._reconnect_delay = None
            self._reconnect_delay_max = None

    # Properties with getters
    @property
    def coil_size(self) -> CoilSize:
        return self._coil_size

    @property
    def discrete_input_size(self) -> DiscreteInputSize:
        return self._discrete_input_size

    @property
    def input_register_size(self) -> InputRegisterSize:
        return self._input_register_size

    @property
    def holding_register_size(self) -> HoldingRegisterSize:
        return self._holding_register_size

    @property
    def timeout(self) -> Timeout:
        return self._timeout

    @property
    def retries(self) -> Retries:
        return self._retries

    @property
    def reconnect_delay(self) -> ReconnectDelay:
        return self._reconnect_delay

    @property
    def reconnect_delay_max(self) -> ReconnectDelayMax:
        return self._reconnect_delay_max

    # Setter methods with validation
    def set_coil_size(self, coil_size: CoilSize):
        assert isinstance(coil_size, CoilSize), "Invalid coil size value"
        self._coil_size = coil_size
        return self

    def set_discrete_input_size(self, discrete_input_size: DiscreteInputSize):
        assert isinstance(discrete_input_size, DiscreteInputSize), "Invalid discrete input size value"
        self._discrete_input_size = discrete_input_size
        return self

    def set_input_register_size(self, input_register_size: InputRegisterSize):
        assert isinstance(input_register_size, InputRegisterSize), "Invalid input register size value"
        self._input_register_size = input_register_size
        return self

    def set_holding_register_size(self, holding_register_size: HoldingRegisterSize):
        assert isinstance(holding_register_size, HoldingRegisterSize), "Invalid holding register size value"
        self._holding_register_size = holding_register_size
        return self

    def set_timeout(self, timeout: Timeout):
        assert isinstance(timeout, Timeout), "Invalid timeout value"
        self._timeout = timeout
        return self

    def set_retries(self, retries: Retries):
        assert isinstance(retries, Retries), "Invalid retries value"
        self._retries = retries
        return self

    def set_reconnect_delay(self, reconnect_delay: ReconnectDelay):
        assert isinstance(reconnect_delay, ReconnectDelay), "Invalid reconnect delay value"
        self._reconnect_delay = reconnect_delay
        return self

    def set_reconnect_delay_max(self, reconnect_delay_max: ReconnectDelayMax):
        assert isinstance(reconnect_delay_max, ReconnectDelayMax), "Invalid reconnect delay max value"
        self._reconnect_delay_max = reconnect_delay_max
        return self
