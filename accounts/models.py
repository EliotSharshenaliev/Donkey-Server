from asgiref.sync import sync_to_async
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.validators.validator import UnicodeNumberIdCardValidator


class RegisterBox(models.Model):
    created_at = models.DateTimeField(auto_created=True, auto_now=True)
    isFinish = models.BooleanField(default=False)

    def __str__(self):
        return str(self.created_at)


class UserToRegister(models.Model):
    box = models.ForeignKey(RegisterBox, on_delete=models.CASCADE)
    email = models.EmailField(max_length=80)
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=32)
    isDone = models.BooleanField(default=False, verbose_name="User has been registred")

    def __str__(self):
        return str(self.username)


number_passport_validator = UnicodeNumberIdCardValidator()


class UserModel(AbstractUser, PermissionsMixin):
    isOnline = models.BooleanField(
        default=False,
        verbose_name="Online",
        help_text=_(
            "User can connect to server using socket. Its connection will be online or offline"
        )
    )
    passport_number = models.CharField(
        _("Password number"),
        max_length=9,
        validators=[number_passport_validator],
        blank=True
    )

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.username

    @sync_to_async
    def set_online(self):
        self.isOnline = not self.isOnline
        self.save()

    @sync_to_async
    def set_offline(self):
        self.isOnline = not self.isOnline
        self.save()
