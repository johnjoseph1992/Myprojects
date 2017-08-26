# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-22 09:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stk', '0007_stkitemdetails_currentstatusid'),
    ]

    operations = [
        migrations.AddField(
            model_name='stkoutgoing',
            name='oldoriginalstatusid',
            field=models.ForeignKey(db_column='oldoriginalstatusid', default=1, on_delete=django.db.models.deletion.CASCADE, to='stk.stkCurrentStatus'),
        ),
    ]
