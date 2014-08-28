# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_auto_20140822_1003'),
        ('minute_in_time', '0001_initial'),
        ('predictions', '0005_rename_prediction_to_tide_prediction_20140826_1542'),
    ]

    operations = [
        migrations.CreateModel(
            name='SurgePrediction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('surge_level', models.FloatField(help_text='The predicted additional height on top of the tide prediction due to other conditions such as weather.')),
                ('location', models.ForeignKey(to='locations.Location')),
                ('minute', models.ForeignKey(to='minute_in_time.Minute')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='surgeprediction',
            unique_together=set([('location', 'minute')]),
        ),
    ]
