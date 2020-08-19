# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-08-19 10:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20200817_1933'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userfootball',
            name='shield',
        ),
        migrations.AddField(
            model_name='userfootball',
            name='size',
            field=models.CharField(choices=[('Small', 'S'), ('Medium', 'M'), ('Large', 'L'), ('Extra Large', 'XL')], default='Medium', max_length=12),
        ),
    ]
