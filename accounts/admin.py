from django.contrib import admin

from accounts.models import UserToRegister
from django.contrib.auth.admin import UserAdmin
from .models import UserModel
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import gettext_lazy as _


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserModel


class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm

    fieldsets = (
                    (None, {"fields": ("username", "password")}),
                    (_("Personal info"), {"fields": ("first_name", "last_name", "email", "passport_number")}),
                    (
                        _("Permissions"),
                        {
                            "fields": (
                                "is_active",
                                "is_staff",
                                "is_superuser",
                                "groups",
                                "user_permissions",
                            ),
                        },
                    ),
                    (_("Important dates"), {"fields": ("last_login", "date_joined")}),
                ) + (
                    (_("User Statuses"), {'fields': ('isOnline',)}),
                )


admin.site.register(UserToRegister)
admin.site.register(UserModel, MyUserAdmin)
