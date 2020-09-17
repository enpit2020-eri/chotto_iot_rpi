from dataclasses import asdict
from typing import Optional

from chotto_iot.sensor_data.sensor_data_type.sensor_data import SensorData
from chotto_iot.sensor_data.sensor_data_type.sensor_data_acc_gyro import SensorDataAccGyro
from chotto_iot.sensor_data.sensor_data_type.sensor_data_geo_pressure import SensorDataGeoPressure
from chotto_iot.sensor_data.sensor_data_type.sensor_data_temp_humid import SensorDataTempHumid

def signed(hex_str):
    return int.from_bytes(bytes.fromhex(hex_str),"big",signed=True)

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
        gacc_x = signed(sensor_data[8:12])*0.000244
        gacc_y = signed(sensor_data[12:16])*0.000244
        gacc_z = signed(sensor_data[16:20])*0.000244
        gyro_x = signed(sensor_data[20:24])*0.07
        gyro_y = signed(sensor_data[24:28])*0.07
        gyro_z = signed(sensor_data[28:32])*0.07
        beacon_id_model = int(sensor_data[32:34], 16)
        beacon_id_serial = int(sensor_data[34:40], 16)
        # print(SensorDataAccGyro(beacon_id_serial, rssi, gacc_x, gacc_y, gacc_z, gyro_x, gyro_y, gyro_z))
        return SensorDataAccGyro(f"{beacon_id_model:02X}{beacon_id_serial:06d}", rssi, gacc_x, gacc_y, gacc_z, gyro_x,
                                 gyro_y, gyro_z)

    def parse_geo_pre(self, sensor_data, rssi):
        geo_x = signed(sensor_data[8:12])*0.00058*10
        geo_y = signed(sensor_data[12:16])*0.00058*10
        geo_z = signed(sensor_data[16:20])*0.00058*10
        pre = int(sensor_data[20:26], 16)/4096.0
        beacon_id_model = int(sensor_data[32:34], 16)
        beacon_id_serial = int(sensor_data[34:40], 16)
        return SensorDataGeoPressure(f"{beacon_id_model:02X}{beacon_id_serial:06d}", rssi, geo_x, geo_y, geo_z, pre)

    def parse_temp_hum(self, sensor_data, rssi):
        temp = signed(sensor_data[8:12])/100.0
        humid = int(sensor_data[12:16], 16)/100.0
        beacon_id_model = int(sensor_data[32:34], 16)
        beacon_id_serial = int(sensor_data[34:40], 16)
        return SensorDataTempHumid(f"{beacon_id_model:02X}{beacon_id_serial:06d}", rssi, temp, humid)


if __name__ == '__main__':
    parser = SensorDataParser()

    # parser, parse xyz!

    test_data_list = [
        # "AA10004012342345345645675678678911222222",
        # "BB100041FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
        # "CC100031FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
        # "FF1000BBFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
        # "FFBBBB40FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
        # "FFBBBBBBFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
        #0000000000111111111122222222223333333333
        #0123456789012345678901234567890123456789
        "a41000310a141d920000000000000000ba0000d0"
    ]

    for test_data in test_data_list:
        sensor_data = parser.parse(test_data, 124)
        print(f"{test_data=}")
        print(f"{sensor_data=}")

        if sensor_data:
            print(f"{asdict(sensor_data)=}")

        print("")
