# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_auto_20140822_1003'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocationStatusConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tide_predictions_alerts_disabled_until', models.DateTimeField(help_text='After this date/time, turn on alerts for tide predictions at this location. Set to blank to turn on immediately.', null=True, blank=True)),
                ('surge_predictions_alerts_disabled_until', models.DateTimeField(help_text='After this date/time, turn on alerts for surge predictions at this location. Set to blank to turn on immediately.', null=True, blank=True)),
                ('observations_alerts_disabled_until', models.DateTimeField(help_text='After this date/time, turn on alerts for observations at this location. Set to blank to turn on immediately.', null=True, blank=True)),
                ('location', models.OneToOneField(related_name='status_config', to='locations.Location')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
