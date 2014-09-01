# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('predictions', '0006_add_surge_prediction_20140827_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surgeprediction',
            name='minute',
            field=models.ForeignKey(related_name='surge_predictions', to='minute_in_time.Minute'),
        ),
        migrations.AlterField(
            model_name='tideprediction',
            name='minute',
            field=models.ForeignKey(related_name='predictions', to='minute_in_time.Minute'),
        ),
    ]
