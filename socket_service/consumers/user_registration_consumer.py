import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from socket_service.models import UserDeviceTasks
from worker_service.serializer import UserDevicesSerializer


class RegisterConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.group_name = "register_group_name"
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "on_handle_state_list_send",
                "data_list": await self.get_data_from_db(),
            }
        )
        await self.accept()

    @sync_to_async
    def get_data_from_db(self):
        # query_set = UserDeviceTasks.objects.filter(isDeviceConnected=True).order_by(('isDeviceConnected'))
        query_set = UserDeviceTasks.objects.all()
        serialized_data = UserDevicesSerializer(query_set, many=True)
        return serialized_data.data

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "on_handle_state_list_send",
                "data_list": [data]
            }
        )

    async def on_handle_state_list_send(self, event):
        await self.send(json.dumps(event))

    async def on_handle_state_object_send(self, event):
        await self.send(json.dumps(event))
