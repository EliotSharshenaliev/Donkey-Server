import json
import os
import sys
import time

import django
from loguru import logger
import websocket


class Donkey:
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
