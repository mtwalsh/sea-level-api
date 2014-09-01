# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observation',
            name='location',
            field=models.ForeignKey(related_name='observations', to='locations.Location'),
        ),
        migrations.AlterField(
            model_name='observation',
            name='minute',
            field=models.ForeignKey(related_name='observations', to='minute_in_time.Minute'),
        ),
    ]
