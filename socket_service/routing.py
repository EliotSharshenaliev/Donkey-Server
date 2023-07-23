from django.urls import re_path

from .consumers import client_consumer, table_consumer, bot_consumer

websocket_urlpatterns = [
    re_path(r"ws/integration/(?P<room_name>\w+)/$", table_consumer.CoreConsumer.as_asgi()),
    re_path(r"ws/client/(?P<user_id>\w+)/$", client_consumer.ClientConsumer.as_asgi()),
    re_path(r"ws/bot/(?P<user_id>\w+)/$", bot_consumer.BotUpdateConsumer.as_asgi())
]