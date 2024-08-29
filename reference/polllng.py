class MVHR(Device):
    def __init__(self, config_loader: ConfigLoader, modbus_factory: ModbusFactory):
        super().__init__(config_loader)
        self._modbus_factory = modbus_factory
        self._stop_event = asyncio.Event()

    @property
    @abstractmethod
    def modbus(self) -> ModbusInterface:
        pass

    @abstractmethod
    async def read_data(self)-> MVHRRepositoryInterface:
        pass

    async def poll_data(self, interval=1.0):
        while not self._stop_event.is_set():
            await self.read_data()
            await asyncio.sleep(interval)

    async def start(self):
        """
        Start the MVHR device connection process.
        """
        try:
            await self.modbus.connect()
            self._state_manager.update_state(operational_states={MVHR_RUNNING: True})
            await self.poll_data()


        except Exception as e:
            self._state_manager.update_state(
                operational_states={MVHR_RUNNING: False},
                triggered_rules={MVHR_START_FAILURE: str(e)}
            )

    async def stop(self):
        self._stop_event.set()
        await self.modbus.disconnect()  # Assuming there is a disconnect method
        self._state_manager.update_state(operational_states={MVHR_RUNNING: False})