from dataclasses import dataclass, asdict

from chotto_iot.sensor_data.sensor_data_type.sensor_data import SensorData


@dataclass
class SensorDataTempHumid(SensorData):
    temperature: float
    humid: float


if __name__ == '__main__':
    data = SensorDataTempHumid('test', 100, 25.11, 30.12)
    print(data)

    values = asdict(data)
    print(values)
