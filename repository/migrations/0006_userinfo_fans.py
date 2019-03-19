# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-08-03 11:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0005_auto_20180803_1928'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='fans',
            field=models.ManyToManyField(related_name='f', through='repository.UserFans', to='repository.UserInfo', verbose_name='粉丝们'),
        ),
    ]
