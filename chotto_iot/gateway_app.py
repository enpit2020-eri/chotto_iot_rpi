from chotto_iot.bluetooth.bluetooth_manager import BluetoothManager
from chotto_iot.bluetooth.bluetooth_manager_callback import BluetoothManagerCallback
from chotto_iot.mqtt.mqtt_manager import MqttManager
from chotto_iot.mqtt.mqtt_manager_callback import MqttManagerCallback
from chotto_iot.sensor_data.sensor_data_parser import SensorDataParser
from bleakWrapper.scan_result import ScanResult

HOST_ADDRESS = "localhost"
HOST_PORT = 1883


class GatewayApp(BluetoothManagerCallback, MqttManagerCallback):
    def __init__(self):
        self.mqtt_manager = MqttManager(HOST_ADDRESS, HOST_PORT)
        self.mqtt_manager.callback = self

        self.sensor_data_parser = SensorDataParser()

        self.bluetooth_manager = BluetoothManager()
        self.bluetooth_manager.callback = self

    def start_control(self):
        self.mqtt_manager.start_connection()

    def on_connected(self):
        self.bluetooth_manager.start_scan()

    def on_received_data(self, adv_data: ScanResult):
        data = adv_data.manufacturer_data_map.get("010b")
        if data is None:
            return

        print(f"{adv_data=}")

        rssi = adv_data.rssi

        sensor_data = self.sensor_data_parser.parse(data, rssi)
        if sensor_data is None:
            return

        self.mqtt_manager.send_sensor_data(sensor_data)


if __name__ == '__main__':
    app = GatewayApp()

    app.start_control()

    app.mqtt_manager.client.loop_forever()

