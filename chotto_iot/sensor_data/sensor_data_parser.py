from dataclasses import asdict
from typing import Optional

from chotto_iot.sensor_data.sensor_data_type.sensor_data import SensorData
from chotto_iot.sensor_data.sensor_data_type.sensor_data_acc_gyro import SensorDataAccGyro
from chotto_iot.sensor_data.sensor_data_type.sensor_data_geo_pressure import SensorDataGeoPressure
from chotto_iot.sensor_data.sensor_data_type.sensor_data_temp_humid import SensorDataTempHumid


class SensorDataParser:
    # + パース(advData): Optional[SensorData]
    """
        def sensor_data_split(self,data):
        sensordata = data
        pedometer = sensordata[0:36]
        acc_gyro = sensordata[36:76]
        geo_pre = sensordata[76:110]
        temp_hum = sensordata[0:24]
    """

    def parse(self, sensor_data: str, rssi: int) -> Optional[SensorData]:
        checksum = sensor_data[0:2]
        beacon_head = sensor_data[2:6]
        beacon_type = sensor_data[6:8]

        if beacon_head != "1000":
            # print("Beacon Head error!")
            return None

        if beacon_type == "40":
            return self.parse_acc_gyro(sensor_data, rssi)
        elif beacon_type == "41":
            return self.parse_geo_pre(sensor_data, rssi)
        elif beacon_type == "31":
            return self.parse_temp_hum(sensor_data, rssi)
        else:
            # print("Beacon type error!")
            return None
        # print(gacc_x)

    def parse_acc_gyro(self, sensor_data, rssi):
        gacc_x = int(sensor_data[8:12], 16)
        gacc_y = int(sensor_data[12:16], 16)
        gacc_z = int(sensor_data[16:20], 16)
        gyro_x = int(sensor_data[20:24], 16)
        gyro_y = int(sensor_data[24:28], 16)
        gyro_z = int(sensor_data[28:32], 16)
        beacon_id_model = int(sensor_data[32:34], 16)
        beacon_id_serial = int(sensor_data[34:40], 16)
        # print(SensorDataAccGyro(beacon_id_serial, rssi, gacc_x, gacc_y, gacc_z, gyro_x, gyro_y, gyro_z))
        return SensorDataAccGyro(f"{beacon_id_model:02X}{beacon_id_serial:06d}", rssi, gacc_x, gacc_y, gacc_z, gyro_x,
                                 gyro_y, gyro_z)

    def parse_geo_pre(self, sensor_data, rssi):
        geo_x = int(sensor_data[8:12], 16)
        geo_y = int(sensor_data[12:16], 16)
        geo_z = int(sensor_data[16:20], 16)
        pre = int(sensor_data[20:26], 16)
        beacon_id_model = int(sensor_data[26:28], 16)
        beacon_id_serial = int(sensor_data[28:34], 16)
        return SensorDataGeoPressure(f"{beacon_id_model:02X}{beacon_id_serial:06d}", rssi, geo_x, geo_y, geo_z, pre)

    def parse_temp_hum(self, sensor_data, rssi):
        temp = int(sensor_data[8:12], 16)
        humid = int(sensor_data[12:16], 16)
        beacon_id_model = int(sensor_data[16:18], 16)
        beacon_id_serial = int(sensor_data[18:24], 16)
        return SensorDataTempHumid(f"{beacon_id_model:02X}{beacon_id_serial:06d}", rssi, temp, humid)


if __name__ == '__main__':
    parser = SensorDataParser()

    # parser, parse xyz!

    test_data_list = [
        "FF100035FFFFFFFFFFFFFFFFFFFFFFFFFFFF",
        "FF100040FFFFFFFFFFFFFFFFFFFFFFFFFFFF",
        "FF100041FFFFFFFFFFFFFFFFFFFFFFFFFFFF",
        "FF100031FFFFFFFFFFFFFFFFFFFFFFFFFFFF",
        "FF1000BBFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
        "FFBBBB40FFFFFFFFFFFFFFFFFFFFFFFFFFFF",
        "FFBBBBBBFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
    ]

    for test_data in test_data_list:
        sensor_data = parser.parse(test_data, 124)
        print(f"{test_data=}")
        print(f"{sensor_data=}")

        if sensor_data:
            print(f"{asdict(sensor_data)=}")

        print("")
