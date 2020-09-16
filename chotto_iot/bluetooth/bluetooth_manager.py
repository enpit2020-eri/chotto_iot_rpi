from typing import Callable, Optional
from bleakWrapper.scan_result import ScanResult
from chotto_iot.bluetooth.bluetooth_manager_callback import BluetoothManagerCallback


if __name__ == '__main__':
    class BleakWrapperSimpleScanner:
        on_received: Optional[Callable[[ScanResult], None]] = None

        def start(self):
            self.on_received("dummy data")
else:
    from bleakWrapper.simpleScanner import BleakWrapperSimpleScanner


class BluetoothManager:
    def __init__(self):
        self.callback: Optional[BluetoothManagerCallback] = None

        self.scanner = BleakWrapperSimpleScanner()
        self.scanner.on_received = self.detected

    def detected(self, data: ScanResult):
        callback = self.callback
        if callback is not None:
            callback.on_received_data(data)

    def start_scan(self):
        self.scanner.start()


if __name__ == '__main__':  ##GatewayApp
    class User(BluetoothManagerCallback):
        def on_received_data(self, adv_data: ScanResult):
            print(f"on_received_data")


    user = User()

    manager = BluetoothManager()
    manager.callback = user

    manager.start_scan()
