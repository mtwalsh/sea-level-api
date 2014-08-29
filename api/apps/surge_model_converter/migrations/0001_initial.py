# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_auto_20140822_1003'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('surge_model_name', models.CharField(help_text='The 4-character code used by the surge model to identify this location.', max_length=4, validators=[django.core.validators.RegexValidator('^[A-Z]{4}$', 'Only four-letter uppercase names are allowed.')])),
                ('location', models.ForeignKey(help_text='The location to which this surge-model location relates', to='locations.Location')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
