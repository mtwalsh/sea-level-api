# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_auto_20140822_1003'),
        ('minute_in_time', '0001_initial'),
        ('predictions', '0004_auto_20140806_1721'),
        ('sea_levels', '0001_initial'),  # manual SQL view
    ]

    operations = [
        migrations.RenameModel(
            'Prediction',
            'TidePrediction'
        ),
    ]
