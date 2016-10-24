# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-20 08:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_online', models.BooleanField(default=False)),
                ('steam_id', models.CharField(default='null', max_length=29)),
                ('bnet_id', models.CharField(default='null', max_length=19)),
                ('friends', models.ManyToManyField(blank=True, related_name='_player_friends_+', to='player_acct.Player')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
