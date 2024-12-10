from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from users.validators import reserved_names_validator

username_validator = UnicodeUsernameValidator()

class UserModel(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=(username_validator, reserved_names_validator)
    )
    email = models.EmailField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30, verbose_name="Имя")
    last_name = models.CharField(max_length=30, verbose_name="Фамилия")
    is_active = models.BooleanField(default=True, verbose_name="Доступен")

    class Meta:
        db_table='user'
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering=("username",)
    
    def __str__(self):
        return self.get_full_name()
    
