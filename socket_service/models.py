import random
import uuid

from django.db import models


class UserDeviceTasks(models.Model):
    user_info = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    login_status = models.BooleanField(default=False)
    random_numbers = models.IntegerField(default=random.randint(1000, 9999))
    deviceId = models.UUIDField(default=uuid.uuid4, unique=True)
    isDeviceConnected = models.BooleanField(default=False)
    isBotConnected = models.BooleanField(default=False)
    key = models.IntegerField(unique=True, default=random.randint(1, 9999))

    def __str__(self):
        return str(self.user_info)

    class Meta:
        ordering = ["deviceId"]



