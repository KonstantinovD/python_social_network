# Generated by Django 3.1 on 2021-02-14 11:02

from django.db import migrations, models
import django.utils.timezone
import markdownx.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('mod_date', models.DateTimeField(blank=True, null=True)),
                ('title', models.CharField(max_length=50)),
                ('body', markdownx.models.MarkdownxField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]