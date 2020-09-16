from abc import ABC, abstractmethod


class MqttManagerCallback(ABC):
    @abstractmethod
    def on_connected(self):
        pass
