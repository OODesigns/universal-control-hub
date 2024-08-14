from abc import ABC


class Device(ABC):
    def __init__(self, store):
        self.name = None
        self.store = store

