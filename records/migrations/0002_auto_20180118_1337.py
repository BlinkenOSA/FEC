# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-18 13:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fecentity',
            name='origin',
        ),
        migrations.AddField(
            model_name='fecentity',
            name='associated_corporations',
            field=models.ManyToManyField(related_name='associated_corporations', to='records.Corporation'),
        ),
        migrations.AddField(
            model_name='fecentity',
            name='associated_people',
            field=models.ManyToManyField(related_name='associated_people', to='records.Person'),
        ),
        migrations.AddField(
            model_name='fecentity',
            name='countries',
            field=models.ManyToManyField(to='records.Country'),
        ),
        migrations.AddField(
            model_name='fecentity',
            name='place',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='records.Place'),
        ),
        migrations.AddField(
            model_name='fecentity',
            name='subject_corporations',
            field=models.ManyToManyField(related_name='subject_corporations', to='records.Corporation'),
        ),
        migrations.AddField(
            model_name='fecentity',
            name='subject_people',
            field=models.ManyToManyField(related_name='subject_people', to='records.Person'),
        ),
    ]
