# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-08-05 15:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0008_auto_20180805_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trouble',
            name='ctime',
            field=models.DateTimeField(verbose_name='创建时间'),
        ),
    ]
