import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from socket_service.models import Bot
from socket_service.serializers import CurrentBotSerializer

channel_layer = get_channel_layer()
UserModel = get_user_model()


async def send_message(channel_layer, channel_name, message):
    await channel_layer.group_send(
        channel_name, message
    )


@receiver(post_save, sender=Bot)
def send_bot_state_to_users(sender, instance, **kwargs):
    room_group_name = "chat_%s" % instance.user
    serialied_data = CurrentBotSerializer(instance)
    message = {
        "type": "send_message",
        "message": serialied_data.data
    }
    async_to_sync(send_message)(
        channel_layer,
        room_group_name, message
    )
