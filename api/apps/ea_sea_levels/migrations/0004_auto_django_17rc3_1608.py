# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ea_sea_levels', '0003_auto_20140822_1007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurement',
            name='station',
            field=models.ForeignKey(related_name='measurements', to='ea_sea_levels.Station'),
        ),
    ]
