# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-15 18:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Predictlog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('suku', models.CharField(max_length=250)),
                ('prob_men', models.FloatField()),
                ('prob_women', models.FloatField()),
                ('feedback', models.CharField(max_length=1)),
                ('feedback_reason', models.CharField(max_length=500)),
                ('api_consumer', models.CharField(max_length=1000)),
                ('client_ip', models.CharField(max_length=50)),
            ],
        ),
    ]
