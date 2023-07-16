from django.db import models


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
