# Generated by Django 3.2.3 on 2023-06-01 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0003_auto_20230601_2045'),
    ]

    operations = [
        migrations.AddField(
            model_name='datasource',
            name='is_archive',
            field=models.BooleanField(default=False),
        ),
    ]