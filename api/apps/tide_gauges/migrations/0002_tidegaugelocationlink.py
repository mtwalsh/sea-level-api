# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_auto_20140822_1003'),
        ('tide_gauges', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TideGaugeLocationLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.CharField(max_length=100, blank=True)),
                ('location', models.OneToOneField(to='locations.Location')),
                ('tide_gauge', models.OneToOneField(to='tide_gauges.TideGauge')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
