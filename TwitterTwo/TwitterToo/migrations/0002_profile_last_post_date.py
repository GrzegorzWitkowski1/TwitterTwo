# Generated by Django 4.2.5 on 2023-09-21 14:07

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TwitterToo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='last_post_date',
            field=models.DateTimeField(auto_now=True, verbose_name=django.contrib.auth.models.User),
        ),
    ]
