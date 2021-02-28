# Generated by Django 3.1 on 2021-02-27 11:11

import django.contrib.postgres.fields.hstore
from django.db import migrations
from django.contrib.postgres.operations import HStoreExtension


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_contact'),
    ]

    operations = [
        HStoreExtension(),
        migrations.AddField(
            model_name='profile',
            name='params',
            field=django.contrib.postgres.fields.hstore.HStoreField(default={'show_name': 'true', 'show_nickname': 'false'}),
        ),
    ]