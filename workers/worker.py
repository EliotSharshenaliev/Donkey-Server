import json
import os
import sys
import time

import django
from loguru import logger
import websocket


class Donkey:
    """
    Класс Donkey представляет осла.

    Атрибуты:
    - Cookie Jar (http.cookiejar.CookieJar): Для хранение куки авторизованной сессии.
    - Requests Session (requests.Session): Для работы http сессиями
    - isStop (Boolean): Для остановки программы в случае если не будет валидным manifest.json
    Методы:
    - sound(): Воспроизводит звук, характерный для осла.

    Пример использования:
    ```
    donkey = Donkey("127.0.0.1", debug_file: str = "user/path/to/log/file")
    donkey.sound()  # Выводит: "И-а-а-а!"
    donkey.eat("морковь")  # Выводит: "Бурундук ест морковь."
    ```

    """

    def __init__(self):
        self.ws = None
        logs_file = sys.argv[2]
        logger.add(f"static/logs/{logs_file}", format="{time} {level} {message}")
        self.deviceId = sys.argv[1]
        manifest = json.load(open("workers/manifest.json"))
        self.connect_ws(manifest.get("host"), manifest.get("port"), deviceId=self.deviceId)
        self.work()

    def connect_ws(self, host, port, deviceId):
        try:
            logger.debug(
                f"WS connecting to the ... {host}:{port}"
            )
            url = f"ws://{host}:{port}/ws/client/client_room/?deviceId={deviceId}&is_client=false"
            self.ws = websocket.create_connection(url)
        except Exception as e:
            logger.error(e.args)

    def work(self):
        while True:
            logger.warning("im working")
            time.sleep(5)


if __name__ == "__main__":
    Donkey()
