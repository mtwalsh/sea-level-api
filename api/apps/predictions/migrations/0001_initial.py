# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField()),
                ('tide_height', models.DecimalField(help_text='The predicted height in metres of the tidal component of the sea level.', max_digits=4, decimal_places=2)),
                ('location', models.ForeignKey(to='locations.Location', to_field='id')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='prediction',
            unique_together=set([('location', 'datetime')]),
        ),
    ]
