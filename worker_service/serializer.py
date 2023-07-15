from rest_framework import serializers
from socket_service.models import UserDeviceTasks


class UserDeviceSerializer(serializers.ModelSerializer):
    user_info = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    def create(self, validated_data):
        user_info = validated_data.pop('user_info')
        email = validated_data.pop('email')
        user = UserDeviceTasks.objects.create(user_info=user_info, email=email, **validated_data)
        return user

    class Meta:
        model = UserDeviceTasks
        fields = "__all__"


class UserDevicesSerializer(serializers.ModelSerializer):
    user_info = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    login_status = serializers.BooleanField(read_only=True)
    random_numbers = serializers.IntegerField(read_only=True)

    class Meta:
        model = UserDeviceTasks
        fields = "__all__"
