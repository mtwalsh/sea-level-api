# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('predictions', '0001_initial'),
        ('minute_in_time', '__first__'),
    ]

    operations = [
        migrations.AddField(
            model_name='prediction',
            name='minute',
            field=models.ForeignKey(blank=True, to='minute_in_time.Minute', null=True),
            preserve_default=True,
        ),
    ]
