# Generated by Django 2.0.1 on 2018-02-28 10:01

import core.managers
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'Пользователь с таким именем существует'}, max_length=128, unique=True, verbose_name='Логин (Имя пользователя)')),
                ('email', models.EmailField(error_messages={'unique': 'Пользователь с таким email существует'}, max_length=128, unique=True, verbose_name='Email')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Имеет доступ в админку')),
                ('inn', models.IntegerField(blank=True, default=None, null=True, verbose_name='ИНН')),
                ('account', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Счет')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
            managers=[
                ('objects', core.managers.CustomUserManager()),
            ],
        ),
    ]
