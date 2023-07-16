from django.contrib import admin

from accounts.models import RegisterBox, UserToRegister

admin.site.register(RegisterBox)
admin.site.register(UserToRegister)

