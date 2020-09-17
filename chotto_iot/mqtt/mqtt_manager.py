import paho.mqtt.client as mqtt
from typing import Optional

from chotto_iot.mqtt.mqtt_manager_callback import MqttManagerCallback
from chotto_iot.sensor_data.sensor_data_type.sensor_data import SensorData



class MqttManager:
    def __init__(self, address: str = "127.0.0.1", port: int = 1883):
        self.address = address
        self.port = port

        # MQTTの接続設定
        self.client = mqtt.Client()  # クラスのインスタンス(実体)の作成
        self.client.on_connect = self.on_connect

        # コールバック
        self.callback: Optional[MqttManagerCallback] = None

    def start_connection(self):
        self.client.connect(self.address, self.port, 60)  # 接続先は自分自身

    def on_connect(self, client, userdata, flag, rc):
        callback = self.callback
        if callback is not None:
            callback.on_connected()

    def send_sensor_data(self, sensor_data: SensorData):
        self.client.publish("/sensorData", sensor_data)  # トピック名とメッセージを決めて送信


if __name__ == '__main__':
    class User(MqttManagerCallback):
        def on_connected(self):
            print("test")


    mqtt_manager = MqttManager()
    mqtt_manager.callback = User()

    mqtt_manager.start_connection()

    mqtt_manager.client.loop_forever()
