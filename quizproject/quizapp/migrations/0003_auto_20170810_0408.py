# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-10 04:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0002_school'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizlogin',
            name='city',
            field=models.CharField(default='Kochi', max_length=50),
        ),
        migrations.AddField(
            model_name='quizlogin',
            name='schoolid',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='quizapp.School'),
        ),
        migrations.AddField(
            model_name='quizlogin',
            name='standard',
            field=models.IntegerField(default=1, null=True),
        ),
        migrations.AddField(
            model_name='quizlogin',
            name='usertype',
            field=models.CharField(default='STUDENT', max_length=10),
        ),
    ]
