# Generated by Django 4.2.5 on 2023-09-21 14:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TwitterToo', '0002_profile_last_post_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='last_post_date',
            new_name='last_active_date',
        ),
    ]
