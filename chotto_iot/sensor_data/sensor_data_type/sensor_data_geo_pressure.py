from dataclasses import dataclass, asdict

from chotto_iot.sensor_data.sensor_data_type.sensor_data import SensorData


@dataclass
class SensorDataGeoPressure(SensorData):
    geo_x: float
    geo_y: float
    geo_z: float
    pressure: float


if __name__ == '__main__':
    data = SensorDataGeoPressure('test', 100, 0.11, 0.12, 0.13, 1014.11)
    print(data)

    values = asdict(data)
    print(values)
