# Generated by Django 3.1 on 2021-02-28 08:28

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_profile_favorites'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='favorites',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=list, size=60),
        ),
    ]
