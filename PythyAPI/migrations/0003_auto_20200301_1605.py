# Generated by Django 3.0.3 on 2020-03-01 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PythyAPI', '0002_auto_20200301_0031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='state',
            field=models.CharField(max_length=10),
        ),
    ]
