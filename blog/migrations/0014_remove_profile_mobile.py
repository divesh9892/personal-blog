# Generated by Django 3.0.8 on 2020-08-29 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='mobile',
        ),
    ]
