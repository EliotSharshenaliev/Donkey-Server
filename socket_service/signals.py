import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from worker_service.serializer import UserDevicesSerializer
from .models import UserDeviceTasks

channel_layer = get_channel_layer()


@receiver(post_save, sender=UserDeviceTasks)
def update_states(sender, instance, **kwargs):
    channel_name = 'device_group_name'
    serialized = UserDevicesSerializer(instance)
    message = {
        'type': 'on_handle_state_object_send',
        'data_obj': serialized.data
    }

    async def send_message(channel_layer, channel_name, message):
        await channel_layer.group_send(channel_name, message)

    async_to_sync(send_message)(channel_layer, channel_name, message)
