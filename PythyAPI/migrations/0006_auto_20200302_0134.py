# Generated by Django 3.0.3 on 2020-03-01 17:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PythyAPI', '0005_booking2'),
    ]

    operations = [
        migrations.DeleteModel(
            name='booking2',
        ),
        migrations.RemoveField(
            model_name='users',
            name='created_time',
        ),
    ]
