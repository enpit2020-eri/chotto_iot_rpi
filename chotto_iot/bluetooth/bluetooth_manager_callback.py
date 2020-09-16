from abc import ABC, abstractmethod
from bleakWrapper.scan_result import ScanResult

# interface BluetoothManagerCallback #d4ebff {
class BluetoothManagerCallback(ABC):
    # + データ受信(advData: バイト列)
    @abstractmethod
    def on_received_data(self, adv_data: ScanResult):
        pass
