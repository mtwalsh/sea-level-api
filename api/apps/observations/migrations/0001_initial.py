# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
        ('minute_in_time', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Observation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_interpolated', models.BooleanField(default=False, help_text='Whether the value was interpolated from other points or is an actual observation.')),
                ('sea_level', models.FloatField(help_text='The measured sea level height.')),
                ('location', models.ForeignKey(to='locations.Location')),
                ('minute', models.ForeignKey(to='minute_in_time.Minute')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='observation',
            unique_together=set([('location', 'minute')]),
        ),
    ]
