# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ea_sea_levels', '0002_station_chart_datum_offset'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='measurement',
            options={'ordering': ('station', 'datetime')},
        ),
        migrations.AlterField(
            model_name='measurement',
            name='datetime',
            field=models.DateTimeField(help_text='The date & time at which the measurement was taken'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='measurement',
            field=models.FloatField(help_text='The tide level measurement in metres.'),
        ),
        migrations.AlterField(
            model_name='station',
            name='chart_datum_offset',
            field=models.FloatField(default=4.93, help_text='Number of metres to add to measurements at this station to convert to the Admiralty Chart Datum at this location.'),
        ),
        migrations.AlterField(
            model_name='station',
            name='location',
            field=models.ForeignKey(help_text='The location to which this measurement station relates', to='locations.Location'),
        ),
        migrations.AlterField(
            model_name='station',
            name='site_datum',
            field=models.CharField(help_text='The datum against which a measurement is taken.', max_length=10),
        ),
        migrations.AlterField(
            model_name='station',
            name='station_id',
            field=models.IntegerField(help_text='The EA numeric ID assigned to the station.'),
        ),
        migrations.AlterField(
            model_name='station',
            name='station_name',
            field=models.CharField(help_text='The EA name given to the station.', max_length=50),
        ),
    ]
