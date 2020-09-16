from dataclasses import dataclass, asdict


@dataclass
class SensorData:
    identifier: str
    rssi: int


if __name__ == '__main__':
    data = SensorData('test', 100)
    print(data)

    values = asdict(data)
    print(values)
