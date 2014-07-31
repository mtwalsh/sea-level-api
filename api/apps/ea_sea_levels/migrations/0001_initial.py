# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(help_text=b'The date & time at which the measurement was taken')),
                ('measurement', models.FloatField(help_text=b'The tide level measurement in metres.')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('station_name', models.CharField(help_text=b'The EA name given to the station.', max_length=50)),
                ('station_id', models.IntegerField(help_text=b'The EA numeric ID assigned to the station.')),
                ('site_datum', models.CharField(help_text=b'The datum against which a measurement is taken.', max_length=10)),
                ('location', models.ForeignKey(help_text=b'The location to which this measurement station relates', to='locations.Location')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='measurement',
            name='station',
            field=models.ForeignKey(to='ea_sea_levels.Station'),
            preserve_default=True,
        ),
    ]
