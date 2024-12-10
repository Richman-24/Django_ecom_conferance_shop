from django.conf import settings
from django.core.exceptions import ValidationError


def reserved_names_validator(value):
    """Валидация имени пользователя."""

    if value.lower() in settings.RESERVED_USERNAMES:
        raise ValidationError(
            "Это имя уже занято - используйте другое"
        )