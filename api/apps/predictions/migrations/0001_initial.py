# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField()),
                ('location', models.ForeignKey(to='locations.Location', to_field='id')),
                ('tide_level', models.FloatField(help_text='The predicted height in metres of the tidal component of the sea level above a known datum.')),
            ],
            options={
                'unique_together': set([('location', 'datetime')]),
            },
            bases=(models.Model,),
        ),
    ]
