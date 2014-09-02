# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sea_levels', '0003_add_surge_prediction_20140828_0922'),
    ]

    operations = [
        migrations.CreateModel(
            name='CombinedPredictionObservation',
            fields=[
            ],
            options={
                'managed': False,
            },
            bases=(models.Model,),
        ),
    ]
