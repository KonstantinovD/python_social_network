# Generated by Django 3.1 on 2021-02-14 19:52

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posting', '0002_auto_20210214_2158'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='tags',
        ),
        migrations.AddField(
            model_name='blogpost',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=20), default=[], size=8),
        ),
    ]
