# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-05 19:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Locator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('longitude', models.DecimalField(blank=True, decimal_places=55, max_digits=60, null=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=55, max_digits=60, null=True)),
                ('created', models.DateField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locators', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
