# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '__latest__'),
    ]

    operations = [
        migrations.CreateModel(
            name='TidePrediction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(unique=True)),
                ('height', models.DecimalField(help_text=b'The predicted height in metres of the tidal component of the sea level.', max_digits=4, decimal_places=2)),
                ('location', models.ForeignKey(to='locations.Location', to_field='id')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
