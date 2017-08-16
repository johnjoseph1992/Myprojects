# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-10 04:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0004_auto_20170810_0410'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('qid', models.AutoField(primary_key=True, serialize=False)),
                ('question', models.CharField(max_length=100)),
                ('qtype', models.CharField(max_length=10)),
                ('options', models.CharField(max_length=100)),
                ('correct', models.CharField(max_length=30, null=True)),
            ],
        ),
    ]
