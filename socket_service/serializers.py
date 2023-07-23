from rest_framework import serializers

from socket_service.models import Bot


class CurrentBotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = "__all__"
