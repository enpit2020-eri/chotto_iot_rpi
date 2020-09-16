from dataclasses import dataclass, asdict

from chotto_iot.sensor_data.sensor_data_type.sensor_data import SensorData


@dataclass
class SensorDataAccGyro(SensorData):
    gacc_x: float
    gacc_y: float
    gacc_z: float
    gyro_x: float
    gyro_y: float
    gyro_z: float


if __name__ == '__main__':
    data = SensorDataAccGyro('test', 100, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16)
    print(data)

    values = asdict(data)
    print(values)
