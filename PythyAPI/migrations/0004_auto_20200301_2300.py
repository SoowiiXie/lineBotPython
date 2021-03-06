# Generated by Django 3.0.3 on 2020-03-01 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PythyAPI', '0003_auto_20200301_1605'),
    ]

    operations = [
        migrations.CreateModel(
            name='booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid', models.CharField(default='0', max_length=50)),
                ('place', models.CharField(max_length=30)),
                ('amount', models.CharField(max_length=5)),
                ('timein', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='users',
            name='created_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
