# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-03 03:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='buddycode',
            field=models.CharField(max_length=150, null=True, unique=True, verbose_name='buddycode'),
        ),
    ]
