from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from core.managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(verbose_name='Логин (Имя пользователя)', max_length=128, unique=True,
                                error_messages={'unique': 'Пользователь с таким именем существует'})

    email = models.EmailField(verbose_name='Email', max_length=128, unique=True,
                              error_messages={'unique': 'Пользователь с таким email существует'})

    is_staff = models.BooleanField(verbose_name='Имеет доступ в админку', default=False)

    inn = models.IntegerField(verbose_name='ИНН', default=None, null=True, blank=True)
    account = models.DecimalField(verbose_name='Счет', decimal_places=2, max_digits=10, default=0)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    objects = CustomUserManager()
