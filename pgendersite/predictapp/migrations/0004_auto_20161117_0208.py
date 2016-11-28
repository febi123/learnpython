# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-16 19:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('predictapp', '0003_auto_20161115_1252'),
    ]

    operations = [
        migrations.AddField(
            model_name='predictlog',
            name='highlighted',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='predictlog',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='predictlog', to=settings.AUTH_USER_MODEL),
        ),
    ]
