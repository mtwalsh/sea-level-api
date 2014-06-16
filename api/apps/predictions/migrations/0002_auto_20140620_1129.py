# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('predictions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prediction',
            name='tide_height',
            field=models.FloatField(help_text='The predicted height in metres of the tidal component of the sea level.'),
        ),
    ]
