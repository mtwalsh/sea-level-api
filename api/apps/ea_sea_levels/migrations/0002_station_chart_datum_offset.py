# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ea_sea_levels', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='station',
            name='chart_datum_offset',
            field=models.FloatField(default=4.93, help_text=b'Number of metres to add measurements at this station in to convert to the Admiralty Chart Datum at the given location'),
            preserve_default=True,
        ),
    ]
