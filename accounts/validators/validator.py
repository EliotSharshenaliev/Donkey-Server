from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class UnicodeNumberIdCardValidator(validators.RegexValidator):
    regex = r"^[A-Z]{2}\d{7}$"
    message = _(
        "Enter a valid number id card. This value may contain only letters, "
        "numbers, and characters. Example AC1234567"
    )
    flags = 0