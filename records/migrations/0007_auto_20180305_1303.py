# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-03-05 13:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0006_auto_20180305_1302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fecentity',
            name='internal_note',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='fecentity',
            name='note',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='fecentity',
            name='summary',
            field=models.TextField(blank=True, null=True),
        ),
    ]
