from django.contrib.auth.models import AbstractUser
from django.db import models

from .utils import ADMIN, CLIENT, ROLES, SUPPORT


class User(AbstractUser):
    role = models.CharField(
        choices=ROLES, blank=True, default=CLIENT, max_length=20
    )
    REQUIRED_FIELDS = ['role']

    @property
    def is_client(self):
        return self.role == CLIENT

    @property
    def is_support(self):
        return self.role == SUPPORT

    @property
    def is_admin(self):
        return self.role == ADMIN

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username}'
