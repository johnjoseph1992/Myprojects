# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-09 11:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('schoolid', models.AutoField(primary_key=True, serialize=False)),
                ('startstd', models.IntegerField(default=1)),
                ('endstd', models.IntegerField(default=12)),
                ('schoolname', models.CharField(max_length=50)),
            ],
        ),
    ]