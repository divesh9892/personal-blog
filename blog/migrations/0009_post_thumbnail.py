# Generated by Django 3.0.8 on 2020-08-18 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20200818_1439'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='thumbnail',
            field=models.ImageField(default=0, upload_to='thumbnails/'),
            preserve_default=False,
        ),
    ]
