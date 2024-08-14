from store import Store


class VentilationConfiguration:
    def __init__(self, store: Store):
        self.setpoint_temperature = None
        self.ventilation_mode = None
        self.store = Store
