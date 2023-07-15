import asyncio
import json
import os
import signal
from urllib.parse import parse_qs
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from socket_service.workers.worker import Donkey
from socket_service.models import UserDeviceTasks


class ClientConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.query_set = None
        self.is_client = None
        self.process = None
        self.group_name = None
        self.deviceId = None
        self.donkey = None

    """"""

    '=========================================== Connection side ==========================================='

    """"""

    async def connect(self):
        query_string = self.scope['query_string'].decode()
        query_params = parse_qs(query_string)

        self.deviceId = query_params.get('deviceId', [None])[0]
        self.is_client = True if query_params.get('is_client', [None])[0] == "true" else False
        self.group_name = f'room_{self.deviceId.replace("-", "")}'

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        if self.is_client:
            # await self.build_donkey()
            await self.connect_to_donkey(self.deviceId)

        await self.connect_db()
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "on_handle_state",
                "message": "Client connected" if self.is_client else "Bot Connected"
            }
        )

    # @sync_to_async
    # def build_donkey(self):
    #     try:
    #         self.donkey = Donkey(deviceId=self.deviceId)
    #         self.donkey.start()
    #     except Exception as e:
    #         print(e)

    @sync_to_async
    def connect_db(self):
        query_set = UserDeviceTasks.objects.get(deviceId=self.deviceId)
        if self.is_client:
            query_set.isDeviceConnected = True
            query_set.save()
        else:
            query_set.isBotConnected = True
            query_set.save()
    #
    # # V1 version by subprocess
    async def connect_to_donkey(self, deviceId: str, *args, **kwargs):
        logFile = deviceId + "__debug__.log"
        worker_path = os.path.join(os.getcwd(), "workers", "worker.py")
        command = ['python', worker_path]

        process_command = command + [deviceId, logFile]
        self.process = await asyncio.create_subprocess_exec(*process_command, stdout=asyncio.subprocess.PIPE,
                                                            stderr=asyncio.subprocess.PIPE)

        await self.save_pid(self.process.pid)

    """"""

    '=========================================== Disconnect side ==========================================='

    """"""

    async def disconnect(self, code):
        # await self.disconnection_donkey()
        await self.disconnection()

    # @sync_to_async()
    # def disconnection_donkey(self):
    #     query_set = UserDeviceTasks.objects.get(deviceId=self.deviceId)
    #     if self.is_client:
    #         query_set.isDeviceConnected = False
    #         query_set.save()
    #     else:
    #         query_set.isBotConnected = False
    #         query_set.save()
    #     self.donkey.terminate()

    # V1 version by subprocess
    @sync_to_async
    def disconnection(self):
        query_set = UserDeviceTasks.objects.get(deviceId=self.deviceId)
        if self.is_client:
            query_set.isDeviceConnected = False
            query_set.save()
        else:
            query_set.isBotConnected = False
            query_set.save()

        try:
            if self.is_client:
                self.process.terminate()
        except Exception as e:
            print(e)

    """"""

    '=========================================== Handlers side ==========================================='

    """"""

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "on_handle_state",
                "message": [data]
            }
        )

    async def on_handle_state(self, event):
        await self.send(json.dumps(event))

    @staticmethod
    def url_parse(query_string):
        params_object = parse_qs(query_string)

        for key, value in params_object.items():
            if len(value) == 1:
                params_object[key] = value[0]
            else:
                params_object[key] = value
        return params_object

    @sync_to_async
    def save_pid(self, pid):
        query_set = UserDeviceTasks.objects.get(deviceId=self.deviceId)
        query_set.key = pid
        query_set.save()
