# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-10 04:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0003_auto_20170810_0408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizlogin',
            name='city',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='quizlogin',
            name='schoolid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizapp.School'),
        ),
        migrations.AlterField(
            model_name='quizlogin',
            name='standard',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='quizlogin',
            name='usertype',
            field=models.CharField(max_length=10),
        ),
    ]
