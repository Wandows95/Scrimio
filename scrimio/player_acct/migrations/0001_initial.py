# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-25 22:34
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('username', models.SlugField(default='NotFound<built-in function id>', max_length=15, unique=True)),
                ('is_online', models.BooleanField(default=False)),
                ('steam_id', models.CharField(blank=True, default='null', max_length=29)),
                ('bnet_id', models.CharField(blank=True, default='null', max_length=19)),
                ('friends', models.ManyToManyField(blank=True, related_name='_player_friends_+', to='player_acct.Player')),
            ],
        ),
    ]
