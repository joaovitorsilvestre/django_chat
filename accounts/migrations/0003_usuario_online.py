# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-17 17:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20160617_1652'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='online',
            field=models.BooleanField(default=False),
        ),
    ]