# Generated by Django 2.0 on 2017-12-05 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Corporation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('corporation', models.CharField(max_length=200, unique=True)),
            ],
            options={
                'db_table': 'fec_corporations',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('country', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'db_table': 'fec_countries',
            },
        ),
        migrations.CreateModel(
            name='FECEntity',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('doc_name', models.CharField(max_length=100)),
                ('title', models.CharField(blank=True, max_length=20)),
                ('title_given', models.CharField(max_length=100)),
                ('date', models.DateField(blank=True, null=True)),
                ('pages', models.IntegerField()),
                ('is_coded', models.BooleanField(default=False)),
                ('is_handwritten', models.BooleanField(default=False)),
                ('summary', models.TextField(blank=True)),
                ('note', models.CharField(blank=True, max_length=200)),
                ('internal_note', models.CharField(blank=True, max_length=200)),
                ('origin', models.CharField(max_length=20)),
                ('confidential', models.BooleanField()),
            ],
            options={
                'db_table': 'fec_entities',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('person', models.CharField(max_length=200, unique=True)),
            ],
            options={
                'db_table': 'fec_people',
            },
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('place', models.CharField(max_length=200, unique=True)),
            ],
            options={
                'db_table': 'fec_places',
            },
        ),
    ]
