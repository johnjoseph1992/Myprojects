# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-22 05:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stk', '0002_stkoutgoings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stkitemdetails',
            name='itemoutgoingid',
            field=models.ForeignKey(db_column='itemoutgoingid', null=True, on_delete=django.db.models.deletion.CASCADE, to='stk.stkOutgoings'),
        ),
    ]
