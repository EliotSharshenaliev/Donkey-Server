import dataclasses
import json
import multiprocessing
import random
import threading
import time
import requests


@dataclasses.dataclass
class InterfaceUserDeviceTasks:
    id: int
    user_info: str
    email: str
    login_status: bool
    random_numbers: int
    deviceId: str
    isDeviceConnected: bool
    isBotConnected: bool
    key: int


class Donkey(multiprocessing.Process):
    def __init__(self, deviceId, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = InterfaceUserDeviceTasks(**self.get_user_by_deviceId(deviceId=deviceId))
        self.subprocess = None


    def run(self) -> None:
        self.subprocess = threading.Thread(target=self.random_number, args=[])
        self.subprocess.start()

    def random_number(self):
        while True:
            try:
                random_number = random.randint(1000, 9999)
                self.user.random_numbers = random_number
                url = "{protocol}{host}:{port}/api/v1/tasks/update-device-task/{deviceId}".format(
                    protocol="http://",
                    host="192.168.0.106",
                    port="8000",
                    deviceId=self.user.deviceId
                )
                payload = dataclasses.asdict(self.user)
                requests.post(url=url, data=payload)
                time.sleep(1)
            except Exception as e:
                time.sleep(4)
                print(e)

    @staticmethod
    def get_user_by_deviceId(deviceId):
        try:
            url = "{protocol}{host}:{port}/api/v1/tasks/update-device-task/{deviceId}".format(
                protocol="http://",
                host="192.168.0.106",
                port="8000",
                deviceId=deviceId
            )
            r = requests.get(url=url)
            response: dict = json.loads(r.content)
            return response.get("data")
        except Exception as e:
            print(e)
