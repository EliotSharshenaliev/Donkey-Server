import asyncio
import json
import os
import django
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings

from accounts.models import UserModel
from socket_service.models import Bot

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()


class ClientConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def get_user_by_id(self, pk):
        return UserModel.objects.get(pk=pk)

    @database_sync_to_async
    def get_new_bot_instance(self, pid, **kwargs) -> Bot:
        query_set = Bot(user=self.user, pid=pid, **kwargs)
        query_set.save()
        return query_set

    @database_sync_to_async
    def delete_bot_instance(self):
        return self.bot.delete()

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.bot_patch = settings.PATH_TO_BOT
        self.bot = None
        self.user = None
        self.room_group_name = None
        self.command: list = settings.RUN_SCRIPT_BOT

    async def connect(self):
        """
            Client connect by user_id and will
            create new instance of bot then return pid of process
        """

        # pk using to get user model
        pk = self.scope["url_route"]["kwargs"]["user_id"]
        # try to get user by pk and save it in Consumer instance
        self.user = await self.get_user_by_id(pk=pk)

        if self.user:
            self.room_group_name = "chat_%s" % self.user.username

            # Add user to new layer of channel with specific name - example: "chat_donkey_user"
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            # new instance of bot
            self.bot = await self.run_script_and_get_pid()

            # set online status user
            await self.user.set_online()
            # Confirm connection to real time socket
            return await self.accept()

        # if user not exist with this id than close connection with code 4000
        return self.close(4000)

    async def disconnect(self, code):
        """

            Disconnection will be made using pid on cmd to kill process
            Disconnection state of user will be made synchronium
        """
        # kill process by pid
        await self.delete_process_by_pid()

        # db set user status Online to Offline
        await self.user.set_offline()

        # db set bot insctance will be deleted
        await self.delete_bot_instance()

        # delete user in layer of group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "send_message",
                "message": [data]
            }
        )

    async def send_message(self, event):
        await self.send(json.dumps(event))

    async def run_script_and_get_pid(self):
        try:
            command = self.command + [self.user.username + "__bot__.log", self.user.username]
            process = await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            # this code was'not superb idea
            # stdout, stderr = await process.communicate()
            stderr = "stderr.decode()"
            stdout = "stdout.decode()"
            return await self.get_new_bot_instance(pid=process.pid, stderr=stderr, stdout=stdout)
        except Exception as e:
            print(f"Error running the script: {e}")
            return None

    async def delete_process_by_pid(self):
        try:
            process = await asyncio.create_subprocess_shell(
                f"kill {self.bot.pid}",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            # Wait for the termination of the process
            await process.wait()
            return process.returncode
        except Exception as e:
            print(f"Error deleting the process: {e}")
            return -1
