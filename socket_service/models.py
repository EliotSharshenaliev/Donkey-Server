import random
import uuid

from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models

from accounts.models import UserModel


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


class Bot(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    started_time = models.DateTimeField(_("date joined"), default=timezone.now)
    is_connected = models.BooleanField(default=False)
    pid = models.CharField(max_length=5, unique=True)
    stdout = models.CharField(max_length=255, default="")
    stderr = models.CharField(max_length=255, default="")


    def __str__(self):
        return str(self.user) + "__bot"

