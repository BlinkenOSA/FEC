# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-05-03 09:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0040_page_draft_title'),
        ('pages', '0012_homepage_about_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegularPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('page_body', wagtail.wagtailcore.fields.RichTextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
