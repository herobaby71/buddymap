# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-05 08:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_buddycode'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_updated',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]