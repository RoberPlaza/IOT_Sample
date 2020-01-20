# Generated by Django 2.2.9 on 2020-01-20 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FireAlarm',
            fields=[
                ('_id', models.AutoField(primary_key=True, serialize=False)),
                ('alarm_is_active', models.BooleanField(default=False)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TemperatureMetric',
            fields=[
                ('_id', models.AutoField(primary_key=True, serialize=False)),
                ('temp', models.FloatField(default=0)),
                ('fire_alarm', models.ForeignKey(on_delete='cascade', to='central_server.FireAlarm')),
            ],
        ),
    ]
