import json

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from accounts.models import UserModel
from accounts.serializers import CurrentUserSerializer
from socket_service.models import Bot


class BotUpdateConsumer(AsyncWebsocketConsumer):
    @sync_to_async
    def serializer_user(self, model):
        return CurrentUserSerializer(model).data

    @database_sync_to_async
    def update_user_instance(self, update_data: dict):

        for key, value in update_data.items():
            setattr(self.user_instance, key, value)
        self.user_instance.save(update_fields=list(update_data.keys()))
        return self.user_instance

    @database_sync_to_async
    def get_user_by_id(self, pk):
        return UserModel.objects.get(pk=pk)

    @database_sync_to_async
    def get_bot_by_user(self, user_id):
        return Bot.objects.get(user_id=user_id)

    @database_sync_to_async
    def set_connected(self):
        self.bot_instance.is_connected = True
        return self.bot_instance.save()

    @database_sync_to_async
    def set_disconnected(self):
        self.bot_instance.is_connected = False
        return self.bot_instance.save()

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user_instance = None
        self.bot_instance = None
        self.user_id = None
        self.room_group_name = None

    async def connect(self):
        self.user_id = self.scope["url_route"]["kwargs"]["user_id"]
        self.bot_instance = await self.get_bot_by_user(user_id=self.user_id)
        self.user_instance = await self.get_user_by_id(pk=self.user_id)
        self.room_group_name = "chat_bot_%s" % self.user_instance

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.set_connected()
        await self.accept()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "first_message",
                "message":
                    await self.serializer_user(
                        self.user_instance
                    )
            }
        )

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.set_disconnected()

    async def receive(self, text_data=None, bytes_data=None):
        data: dict = json.loads(text_data)
        await self.channel_layer.group_send(self.room_group_name,data)

    async def send_message(self, event):
        await self.send(json.dumps(event))

    async def first_message(self, event):
        await self.send(json.dumps(event))

    async def update_user(self, event: dict):
        new_user = event.get("message")
        instance = await self.update_user_instance(new_user)
        payload = await self.serializer_user(instance)
        await self.send(json.dumps(payload))
