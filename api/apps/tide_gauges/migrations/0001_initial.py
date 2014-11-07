# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RawMeasurement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(help_text='The date & time (according to the tide gauge) for which the measurement is valid.')),
                ('height', models.FloatField(help_text='The tide gauge measurement in metres.')),
            ],
            options={
                'ordering': ['datetime'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TideGauge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=100, validators=[django.core.validators.RegexValidator('^[a-z0-9-]+$', 'Only lowercase alphanumeric characters and hyphens are allowed.')])),
                ('comment', models.CharField(max_length=100, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='rawmeasurement',
            name='tide_gauge',
            field=models.ForeignKey(related_name='raw_measurements', to='tide_gauges.TideGauge'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='rawmeasurement',
            unique_together=set([('tide_gauge', 'datetime')]),
        ),
    ]
